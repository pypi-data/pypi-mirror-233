#!/usr/bin/env python

import polars as pl
from polars import col
import os
from os import path
import shutil
import typer
from typing import List, Optional


app = typer.Typer()
pl.toggle_string_cache(True)


DATASETS = {
    "P2P Benchmark": [
        {"name": "medium", "num_events": 8350208, "num_partitions": 2},
        {"name": "large", "num_events": 33400832, "num_partitions": 8},
        {"name": "2xlarge", "num_events": 66801664, "num_partitions": 16},
        {"name": "4xlarge", "num_events": 133603328, "num_partitions": 32},
        {"name": "8xlarge", "num_events": 267206656, "num_partitions": 64},
        {"name": "16xlarge", "num_events": 534413312, "num_partitions": 128},
        {"name": "32xlarge", "num_events": 1068826624, "num_partitions": 256},
    ],
    "P2P Records": [
        {"name": "500k_events", "num_events": 16309 * 31, "num_partitions": 1},
        {"name": "1mio_events", "num_events": 16309 * 62, "num_partitions": 1},
        {"name": "2mio_events", "num_events": 16309 * 123, "num_partitions": 1},
        {"name": "5mio_events", "num_events": 16309 * 62 * 5, "num_partitions": 1},
    ],
}


@app.command()
def grow_log(
    events_original: pl.DataFrame,
    events_case_id: str,
    cases_original: pl.DataFrame,
    cases_case_id: str,
    variants_original: pl.LazyFrame,
    dataset_collection: str,
    output_csv: bool,
    output_feather: bool,
    feather_compression: str,
    compression_level: int,
    data_folder: str,
    dataset: Optional[List[str]],
    partitions: int,
    use_internal_format: bool,
    growth_factor: int,
) -> str:
    if use_internal_format:
        events_original = events_original.with_columns(
            [
                col("CaseID").cast(pl.UInt32),
                col("NextCaseID").cast(pl.UInt32),
            ]
        )
        cases_original = cases_original.with_columns([col("CaseID").cast(pl.UInt32)])

    num_cases = events_original.select(events_case_id).unique().height
    num_events = events_original.height
    print(f"Original dataset has {num_events} events and {num_cases} cases.")

    if dataset_collection is not None:
        datasets = DATASETS[dataset_collection]
        if dataset:
            selected_datasets = []
            for d in dataset:
                selected_datasets.append(next(x for x in datasets if x["name"] == d))
        else:
            selected_datasets = datasets
    else:
        growth_factor = growth_factor if growth_factor is not None else 2
        selected_datasets = [
            {
                "name": dataset[0] if len(dataset) > 0 else f"{growth_factor}xdataset",
                "num_events": growth_factor * num_events,
                "num_partitions": partitions if partitions is not None else 1,
            }
        ]

    file_extension = "parquet"
    if output_csv:
        file_extension = "csv"
    elif output_feather:
        file_extension = "feather"
        if feather_compression != "uncompressed":
            file_extension += f".{feather_compression}"

    for dataset in selected_datasets:
        num_partitions = (
            partitions if partitions is not None else dataset["num_partitions"]
        )
        dataset_path = f"{data_folder}/{dataset['name']}"
        if os.path.exists(dataset_path):
            shutil.rmtree(dataset_path)
        os.makedirs(dataset_path)
        if num_partitions > 1:
            os.makedirs(f"{dataset_path}/events.{file_extension}")
            os.makedirs(f"{dataset_path}/cases.{file_extension}")

        growth_factor = int(dataset["num_events"] / num_events)
        partition_size = int(growth_factor / num_partitions)
        partition_index = 1
        print(
            f"Create dataset {dataset['name']} with {dataset['num_events']} (growth factor = {growth_factor}, partition size = {partition_size}*{num_events}={partition_size*num_events})"
        )
        event_dfs = [events_original]
        cases_dfs = [cases_original]
        for i in range(growth_factor - 1):
            print(f"{int((i+1)/(growth_factor-1)*100)} %", end="\r", flush=True)
            if use_internal_format:
                case_id_add = num_cases * (i + 1) + 1
                case_id_new = col(events_case_id) + case_id_add
                internal_cols = (
                    [col("Action"), col("Start"), (col("NextCaseID") + case_id_add)],
                )
                internal_col_names = ["Action", "Start", "NextCaseID"]
            else:
                case_id_new = pl.concat_str([col(events_case_id), pl.lit(f"_{i}")])
                internal_cols = []
                internal_col_names = []

            event_dfs.append(
                events_original.select(
                    [
                        case_id_new,
                        *internal_cols,
                        pl.all().exclude([events_case_id, *internal_col_names]),
                    ]
                )
            )

            if use_internal_format:
                case_id_add = num_cases * (i + 1) + 1
                case_id_new = col(cases_case_id) + case_id_add
            else:
                case_id_new = pl.concat_str([col(cases_case_id), pl.lit(f"_{i}")])

            cases_dfs.append(
                cases_original.select(
                    [
                        case_id_new,
                        pl.all().exclude(cases_case_id),
                    ]
                )
            )
            if (i + 1) % partition_size == 0 or (i + 1) == (growth_factor - 1):
                if num_partitions > 1:
                    events_partition_path = f"{dataset_path}/events.{file_extension}/events_{partition_index}.{file_extension}"
                    cases_partition_path = f"{dataset_path}/cases.{file_extension}/cases_{partition_index}.{file_extension}"
                else:
                    events_partition_path = f"{dataset_path}/events.{file_extension}"
                    cases_partition_path = f"{dataset_path}/cases.{file_extension}"

                events_grown = pl.concat(event_dfs)
                print(f"Write {events_grown.height} rows to {events_partition_path}")
                if not (output_csv or output_feather):
                    events_grown.write_parquet(
                        events_partition_path, compression_level=compression_level
                    )
                elif output_csv:
                    if not use_internal_format:
                        events_export = events_grown
                    else:
                        events_export = events_grown.drop(
                            ["Duration", "NextCaseID", "NextStart"]
                        )
                    events_export.write_csv(events_partition_path)
                else:
                    events_grown.write_ipc(
                        events_partition_path, compression=feather_compression
                    )

                cases_grown = pl.concat(cases_dfs)
                print(f"Write {cases_grown.height} rows to {cases_partition_path}")

                if not (output_csv or output_feather):
                    cases_grown.write_parquet(
                        cases_partition_path, compression_level=compression_level
                    )
                elif output_csv:
                    cases_grown.write_csv(cases_partition_path)
                else:
                    cases_grown.write_ipc(
                        cases_partition_path, compression=feather_compression
                    )
                partition_index += 1
                event_dfs = []
                cases_dfs = []
        if use_internal_format and not (output_csv or output_feather):
            variants_original.collect().write_parquet(
                f"{dataset_path}/variants.{file_extension}"
            )
        elif use_internal_format and output_feather:
            variants_original.collect().write_ipc(
                f"{dataset_path}/variants.{file_extension}",
                compression=feather_compression,
            )

    return dataset_path


@app.command()
def grow_ocel_csv(
    dataset: str = typer.Argument(help="Name of the dataset collection"),
    data_folder: str = typer.Option("./data", help="Data folder"),
):
    dataset_folder = path.join(data_folder, dataset)
    events_original = pl.scan_csv(path.join(dataset_folder, "events.csv"))


if __name__ == "__main__":
    app()
