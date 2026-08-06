"""
Utilities for exporting benchmark results.

Provides helper functions for saving tabular data,
text summaries, and other analysis outputs.
"""

from pathlib import Path

import pandas as pd


def save_dataframe(
    df: pd.DataFrame,
    save_path: str | Path,
) -> None:
    """
    Save a pandas DataFrame as a CSV file.

    Parent directories are created automatically if they
    do not already exist.
    """

    save_path = Path(save_path)

    save_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        save_path,
        index=False,
    )


def load_dataframe(
    save_path: str | Path,
) -> pd.DataFrame:

    return pd.read_csv(
        save_path,
    )


def save_text(
    text: str,
    save_path: str | Path,
) -> None:
    """
    Save plain-text output to a file.

    Parent directories are created automatically if they
    do not already exist.
    """

    save_path = Path(save_path)

    save_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_path.write_text(
        text,
        encoding="utf-8",
    )


def file_exists(
    path: str | Path,
) -> bool:

    return Path(path).exists()


def should_rerun(
    path: str | Path,
    use_cache: bool = True,
) -> bool:

    return (
        not use_cache
        or not file_exists(path)
    )