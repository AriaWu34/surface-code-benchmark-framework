"""
Visualization utilities for runtime benchmarking.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from .common import save_figure


def plot_runtime_scaling(
    distances,
    runtimes: dict[str, dict[str, list[float]]],
    save_path: str | Path | None = None,
) -> None:
    """
    Plot runtime scaling with error bars.

    Parameters
    ----------
    distances
        Code distances.

    runtimes
        Mapping

            {
                "rotated": {
                    "mean": [...],
                    "std": [...],
                },
                "unrotated": {
                    "mean": [...],
                    "std": [...],
                },
            }

    save_path
        Optional output path.
    """

    plt.figure(figsize=(6, 4))

    for label, data in runtimes.items():

        means = data["mean"]
        stds = data["std"]

        plt.errorbar(
            distances,
            means,
            yerr=stds,
            marker="o",
            linewidth=2,
            capsize=4,
            label=label.capitalize(),
        )

        #
        # Annotate mean runtime
        #

        for distance, runtime in zip(
            distances,
            means,
        ):

            plt.annotate(
                f"{runtime:.2f}s",
                (distance, runtime),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
                fontsize=8,
            )

    plt.xlabel(
        "Code distance"
    )

    plt.ylabel(
        "Runtime (s)"
    )

    plt.title(
        "Stim Runtime Scaling"
    )

    plt.grid(
        alpha=0.3,
    )

    plt.legend()

    plt.tight_layout()

    save_figure(save_path)

    plt.close()