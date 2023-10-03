"""
functions to manipulate event logs to create more complex process data
"""

from random import randrange
import polars as pl


def remove_events(events: pl.LazyFrame, number_events_remove: int) -> pl.LazyFrame:
    number_events = events.select(pl.count()).collect()[0, 0]
    new_events = events.collect()
    for _ in range(number_events_remove):
        row_num = randrange(number_events)
        new_events = new_events.slice(0, row_num - 1).vstack(
            new_events.slice(row_num, None)
        )

    return new_events.lazy()


def duplicate_events(
    events: pl.LazyFrame, number_events_duplicate: int
) -> pl.LazyFrame:
    number_events = events.select(pl.count()).collect()[0, 0]
    new_events = events.collect()
    for _ in range(number_events_duplicate):
        row_num = randrange(number_events)
        new_events = (
            new_events.slice(0, row_num)
            .vstack(new_events.slice(row_num, 1))
            .vstack(new_events.slice(row_num, None))
        )

    return new_events.lazy()


def swap_events(events: pl.LazyFrame, number_events_swap: int) -> pl.LazyFrame:
    number_events = events.select(pl.count()).collect()[0, 0]
    new_events = events.collect()
    for _ in range(number_events_swap):
        row_num = randrange(number_events)
        new_events = (
            new_events.slice(0, row_num - 1)
            .vstack(new_events.slice(row_num + 1, 1))
            .vstack(new_events.slice(row_num, 1))
            .vstack(new_events.slice(row_num + 2, None))
        )

    return new_events.lazy()
