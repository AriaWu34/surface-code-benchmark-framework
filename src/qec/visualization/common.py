"""
Shared plotting utilities.
"""

from pathlib import Path

import matplotlib.pyplot as plt


def save_figure(
    save_path: str | Path | None = None,
) -> None:
    """
    Save the current Matplotlib figure.

    Parent directories are created automatically if they
    do not already exist.
    """

    if save_path is None:
        return

    path = Path(save_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
    )

    print(f"Saved figure to {path}")