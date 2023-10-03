import errno
import json
import os
from pathlib import Path
import polars as pl

from apm4py.event_log import EventLog
from apm4py.utils import get_file_by_pattern


def load_log(
    data_folder: Path, csv_separator: str = ",", use_internal_format=False
) -> EventLog:
    event_path = get_file_by_pattern(data_folder, "*[eE]vent*.csv")
    if event_path is not None:
        event_semantics_path = get_file_by_pattern(data_folder, "*[eE]vent*.json")

        if event_semantics_path is None:
            print(
                "Event CSV import requires an event semantics JSON file in the same directory"
            )
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), "*[eE]vent*.json"
            )

        with open(event_semantics_path, "r") as event_semantics_file:
            event_semantics = json.load(event_semantics_file)

        print(f"Loading {event_path}")
        events_original = pl.scan_csv(event_path, separator=csv_separator)

    else:
        event_path = get_file_by_pattern(data_folder, "*[eE]vent*.parquet")
        if event_path is None:
            print("Couldn't find any event file in the dataset directory")
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                "*[eE]vent*.csv | *[eE]vent*.parquet",
            )
        print(f"Loading {event_path}")
        events_original = pl.scan_parquet(event_path)

    cases_path = get_file_by_pattern(data_folder, "*[cC]ase*.csv")
    if cases_path is not None:
        case_semantics_path = get_file_by_pattern(data_folder, "*[cC]ase*.json")
        if case_semantics_path is None:
            print(
                "Case CSV import requires an event semantics JSON file in the same directory"
            )
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), "*[cC]ase*.json"
            )

        with open(case_semantics_path, "r") as case_semantics_file:
            case_semantics = json.load(case_semantics_file)

        print(f"Loading {cases_path}")
        cases_original = pl.scan_csv(cases_path, separator=csv_separator)
    else:
        cases_path = get_file_by_pattern(data_folder, "*[cC]ases*.parquet")
        if cases_path is None:
            print("Couldn't find any cases file in the dataset directory")
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                "*[cC]ases*.csv | *[cC]ases*.parquet",
            )
        print(f"Loading {cases_path}")
        cases_original = pl.scan_parquet(cases_path)

    variants_original = None
    if use_internal_format:
        variants_original = pl.scan_parquet(
            os.path.join(data_folder, "variants.parquet")
        )

    semantics = {"eventSemantics": event_semantics, "caseSemantics": case_semantics}
    (evt_semantics, cse_semantics) = parse_semantics(semantics)

    return EventLog(
        events=events_original,
        event_semantics=evt_semantics,
        cases=cases_original,
        case_semantics=cse_semantics,
        variants=variants_original,
    )


def parse_semantics(semantics: dict[str]):
    def getColumnName(semantics_json, semantics_type, semantic):
        column_names = getColumnNames(semantics_json, semantics_type, semantic)
        column_name = column_names[0] if len(column_names) > 0 else None
        return column_name

    def getTimeFormat(semantics_json, semantics_type, semantic):
        return [
            s["format"]
            for s in semantics_json[semantics_type]
            if s["semantic"] == semantic
        ][0]

    def getColumnNames(semantics_json, semantics_type, semantic):
        return [
            s["name"]
            for s in semantics_json[semantics_type]
            if s["semantic"] == semantic
        ]

    caseid_column = getColumnName(semantics, "eventSemantics", "Case ID")
    action_column = getColumnName(semantics, "eventSemantics", "Action")
    start_column = getColumnName(semantics, "eventSemantics", "Start")
    complete_column = getColumnName(semantics, "eventSemantics", "Complete")
    if complete_column is None:
        complete_column = start_column

    time_format_mapping = {
        "yyyy": "%Y",
        "MM": "%m",
        "dd": "%d",
        "HH": "%H",
        "mm": "%M",
        "ss": "%S",
        ".SSS": "%.3f",
        "Z": "%z",
    }

    time_format = getTimeFormat(semantics, "eventSemantics", "Start")
    for orig_fmt, polars_fmt in time_format_mapping.items():
        time_format = time_format.replace(orig_fmt, polars_fmt)

    categorical_attr = getColumnNames(
        semantics, "eventSemantics", "CategorialAttribute"
    )
    numeric_attr = getColumnNames(semantics, "eventSemantics", "NumericAttribute")

    event_semantics = {
        "caseid_column": caseid_column,
        "action_column": action_column,
        "start_column": start_column,
        "complete_column": complete_column,
        "time_format": time_format,
        "categorical_attr": categorical_attr,
        "numerical_attr": numeric_attr,
    }

    case_semantics = {}
    if "caseSemantics" in semantics:
        cases_caseid_column = getColumnName(semantics, "caseSemantics", "Case ID")
        cases_categorical_attr = getColumnNames(
            semantics, "caseSemantics", "CategorialAttribute"
        )
        cases_numeric_attr = getColumnNames(
            semantics, "caseSemantics", "NumericAttribute"
        )
        case_semantics = {
            "caseid_column": cases_caseid_column,
            "categorical_attr": cases_categorical_attr,
            "numerical_attr": cases_numeric_attr,
        }

    return (event_semantics, case_semantics)
