"""
Threshold analysis visualisations.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from .common import save_figure


def plot_threshold(
    physical_error_rates,
    logical_error_rates_by_distance,
    lattice: str,
    basis: str,
    threshold: float | None = None,
    save_path: str | Path | None = None,
) -> None:
    """
    Plot threshold curves for multiple code distances.
    """

    plt.figure(
        figsize=(6.8, 4.8),
    )

    for (
        distance,
        logical_rates,
    ) in sorted(
        logical_error_rates_by_distance.items()
    ):

        plt.plot(
            physical_error_rates,
            logical_rates,
            marker="o",
            linewidth=2,
            label=f"d={distance}",
        )

    if threshold is not None:

        plt.axvline(
            threshold,
            color="black",
            linestyle="--",
            linewidth=2,
            alpha=0.8,
            label=(
                f"Threshold ≈ "
                f"{100 * threshold:.2f}%"
            ),
        )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel(
        "Physical error rate"
    )

    plt.ylabel(
        "Logical failure rate"
    )

    plt.title(
        "Threshold Estimation\n"
        f"{lattice.capitalize()} Surface Code "
        f"({basis}-Memory)"
    )

    plt.grid(
        which="both",
        linestyle=":",
        alpha=0.4,
    )

    plt.legend(
        title="Code distance",
    )

    plt.tight_layout()

    save_figure(save_path)

    plt.close()