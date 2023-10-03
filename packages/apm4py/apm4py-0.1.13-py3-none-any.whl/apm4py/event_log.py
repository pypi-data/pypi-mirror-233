from dataclasses import dataclass
import json
import os
from pathlib import Path
import polars as pl
from polars import col, LazyFrame
import shutil


@dataclass
class EventLog:
    events: LazyFrame
    cases: LazyFrame
    event_semantics: dict[str]
    case_semantics: dict[str]
    variants: LazyFrame = None

    def caseid_events(self):
        return self.event_semantics["caseid_column"]

    def caseid_cases(self):
        return self.case_semantics["caseid_column"]

    def action_col(self):
        return self.event_semantics["action_column"]

    def start_col(self):
        return self.event_semantics["start_column"]

    def save_log(self, path: Path, file_type: str = "csv"):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        match file_type:
            case "parquet":
                self.events.collect().write_parquet(
                    os.path.join(path, "events.parquet")
                )
                self.cases.collect().write_parquet(os.path.join(path, "cases.parquet"))

            case _:
                self.events.collect().write_csv(os.path.join(path, "events.csv"))
                self.cases.collect().write_csv(os.path.join(path, "cases.csv"))

        self.save_semantics(path)

    def save_semantics(self, path: Path):
        with open(
            os.path.join(path, "event_semantics.json"), "w"
        ) as event_semantics_file:
            json.dump(self.event_semantics, event_semantics_file)

        with open(
            os.path.join(path, "case_semantics.json"), "w"
        ) as case_semantics_file:
            json.dump(self.case_semantics, case_semantics_file)

    def compute_variants(self) -> LazyFrame:
        case_id = self.caseid_events()
        action_col = self.action_col()
        start_col = self.start_col()

        variants_raw = (
            self.events.with_columns(
                [
                    col(case_id).cast(pl.Categorical).cast(pl.UInt16),
                    col(action_col).cast(pl.Categorical),
                    col(start_col).str.strptime(
                        pl.Datetime, format=self.event_semantics["time_format"]
                    ),
                ]
            )
            .groupby(case_id)
            .agg([col(action_col).sort_by(start_col).alias("Variant")])
        )

        self.variants = variants_raw.groupby("Variant").agg([pl.count().alias("Freq")])

        return self.variants
