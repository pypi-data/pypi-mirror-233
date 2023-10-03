import dataclasses
import json
import math
import os
from pathlib import Path
import polars as pl
import shutil
import sys
import typer
from typing import List, Optional
from typing_extensions import Annotated

import apm4py
from apm4py.event_log import EventLog
import apm4py.log_grower
from apm4py.utils import get_file_by_pattern
from apm4py.log_io import load_log
from apm4py.log_manipulation import *

app = typer.Typer()


@app.command()
def upload(
    data_folder: str = typer.Argument(help="Folder where data sets are stored"),
    name: Optional[str] = typer.Option(None, help="Name of the event log"),
    profile: str = typer.Option("default", help="Profile of the Process Mining host"),
    chunk_size: int = typer.Option(
        250000, help="Number of lines to upload in one chunk"
    ),
):
    profile_config = get_profile_config(profile)
    api = apm4py.create_api(**profile_config)
    event_path = get_file_by_pattern(data_folder, "*[eE]vent*.csv")
    event_semantics = get_file_by_pattern(data_folder, "*[eE]vent*.json")
    case_file = get_file_by_pattern(data_folder, "*[cC]ase*.csv")
    case_semantics = get_file_by_pattern(data_folder, "*[cC]ase*.json")

    name = name if name is not None else Path(event_path).stem
    api.upload_event_log_file(
        name=name,
        event_file_path=event_path,
        event_semantics_path=event_semantics,
        case_file_path=case_file,
        case_semantics_path=case_semantics,
        chunk_size=chunk_size,
        show_progress=True,
    )


@app.command()
def list_logs(
    profile: str = typer.Option("default", help="Profile of the Process Mining host"),
):
    profile_config = get_profile_config(profile)
    api = apm4py.create_api(**profile_config)
    logs = api.list_logs()

    if len(logs) > 0:
        pl.Config.set_fmt_str_lengths(100)
        print(
            pl.from_dicts(logs)
            .with_columns(pl.from_epoch("insertedAt", time_unit="ms"))
            .select(["id", "name", "insertedAt"])
            .sort("insertedAt", descending=True)
        )

    else:
        print("No logs available")


def get_profile_config(profile: str):
    apm_dir = os.path.join(os.environ.get("HOME"), ".apm")
    apm_profile_path = os.path.join(os.environ.get("HOME"), ".apm", profile)
    if not os.path.exists(apm_profile_path):
        if not os.path.exists(apm_dir):
            os.mkdir(apm_dir)

        print(f"Profile {profile} does not exists. Please create a profile first.")
        profile = typer.prompt("Name of your profile", default="default")
        if profile == "":
            profile = "default"

        host = typer.prompt("Hostname")
        scheme = typer.prompt("Scheme", default="https")
        port = typer.prompt("Port", default="auto")
        token = typer.prompt("API Token", default="None")
        instance = typer.prompt("Instance", default=2)

        profile_config = {"host": host, "scheme": scheme, "instance": instance}

        if port != "auto":
            profile_config["port"] = port

        if token != "None":
            profile_config["token"] = token

        apm_profile_path = os.path.join(os.environ.get("HOME"), ".apm", profile)
        with open(apm_profile_path, "w") as profile_file:
            json.dump(profile_config, profile_file)

    else:
        with open(apm_profile_path, "r") as profile_file:
            profile_config = json.loads(profile_file.read())

    return profile_config


@app.command()
def grow_log(
    orig_data_folder: Annotated[
        Path, typer.Argument(help="Folder for the original dataset")
    ],
    dataset_collection: Annotated[
        str, typer.Option(help="Name of the dataset collection (P2P_Benchmark|)")
    ] = None,
    output_csv: Annotated[
        bool, typer.Option(help="Output CSV files instead of parquet")
    ] = False,
    output_feather: Annotated[
        bool, typer.Option(help="Output feather files instead of parquet")
    ] = False,
    feather_compression: Annotated[
        str, typer.Option(help="uncompressed|lz4|zstd")
    ] = "uncompressed",
    compression_level: Annotated[
        int, typer.Option(help="File compression level")
    ] = None,
    data_folder: Annotated[
        str, typer.Option(help="Output folder for datasets")
    ] = "./data",
    dataset: Annotated[
        Optional[List[str]],
        typer.Option(help="Only build a specific dataset from collection"),
    ] = None,
    partitions: Annotated[
        int, typer.Option(help="Overwrite num partitions with given number")
    ] = None,
    use_internal_format: Annotated[
        bool,
        typer.Option(help="Use the internally used format with numerical Case IDs"),
    ] = False,
    csv_separator: Annotated[str, typer.Option()] = ",",
    growth_factor: Annotated[
        int,
        typer.Option(
            help="Frequency of appending the log to itself. Only used when no dataset collection is selected.",
        ),
    ] = None,
):
    orig_log = load_log(
        data_folder=orig_data_folder,
        csv_separator=csv_separator,
        use_internal_format=use_internal_format,
    )
    new_dataset_path = apm4py.log_grower.grow_log(
        events_original=orig_log.events.collect(),
        events_case_id=orig_log.caseid_events(),
        cases_original=orig_log.cases.collect(),
        cases_case_id=orig_log.caseid_cases(),
        variants_original=orig_log.variants,
        dataset_collection=dataset_collection,
        output_csv=output_csv,
        output_feather=output_feather,
        feather_compression=feather_compression,
        compression_level=compression_level,
        data_folder=data_folder,
        dataset=dataset,
        partitions=partitions,
        use_internal_format=use_internal_format,
        growth_factor=growth_factor,
    )

    orig_log.save_semantics(new_dataset_path)

    # shutil.copy(case_semantics_path, new_dataset_path)
    # shutil.copy(event_semantics_path, new_dataset_path)


@app.command()
def manipulate_log(
    orig_data_folder: Annotated[
        Path, typer.Argument(help="Folder for the original dataset")
    ],
    data_folder: Annotated[
        str, typer.Option(help="Output folder for datasets")
    ] = "./data",
    dataset_name: Annotated[
        str,
        typer.Option(help="Name of the newly generated dataset"),
    ] = "manipulated_dataset",
    csv_separator: Annotated[str, typer.Option()] = ",",
    use_internal_format: Annotated[
        bool,
        typer.Option(help="Use the internally used format with numerical Case IDs"),
    ] = False,
    number_variants: Annotated[
        int, typer.Option(help="Number of variants yielded by the manipulation")
    ] = None,
):
    orig_log = load_log(
        data_folder=orig_data_folder,
        csv_separator=csv_separator,
        use_internal_format=use_internal_format,
    )

    orig_num_variants = orig_log.compute_variants().collect().height

    if number_variants is not None:
        variant_diff = number_variants - orig_num_variants
        if variant_diff <= 1:
            print(
                f"""
                The event log already has {orig_num_variants} variants.
                You wanted to reach {number_variants}, so there's nothing to do.
                Use --number-variants to yield a larger number of variants.
                """
            )

        new_log = dataclasses.replace(orig_log)
        new_log_path = os.path.join(data_folder, dataset_name)

        while variant_diff > 0:
            num_evts_per_step = math.ceil(variant_diff / 3)

            new_events = new_log.events
            new_events = remove_events(new_events, num_evts_per_step)
            new_events = swap_events(new_events, num_evts_per_step)
            new_events = duplicate_events(new_events, num_evts_per_step)
            new_log.events = new_events

            new_num_variants = new_log.compute_variants().collect().height

            variant_diff = number_variants - new_num_variants

    if new_num_variants is None:
        new_num_variants = new_log.compute_variants().collect().height

    print(
        f"""
          Saving new event log with 
          {new_num_variants} variants (orig: {orig_num_variants}) and
          {new_log.events.collect().height} events (orig: {orig_log.events.collect().height})
          to {new_log_path}
          """
    )

    new_log.save_log(new_log_path)


def main():
    sys.exit(app())


if __name__ == "__main__":
    main()
