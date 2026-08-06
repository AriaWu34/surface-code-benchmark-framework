"""
Visualization routines for benchmark comparisons.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from .common import save_figure


def plot_decoder_comparison(
    ps,
    pLX_1,
    pLZ_1,
    pLX_ST,
    pLZ_ST,
    save_path=None,
) -> None:
    """
    Compare single-round and space-time MWPM decoding
    for Qiskit reference implementation.
    """

    plt.figure(figsize=(7.5, 5.2))

    plt.plot(
        ps,
        pLX_1,
        "o-",
        label="Logical-X (single round)",
    )

    plt.plot(
        ps,
        pLZ_1,
        "s--",
        label="Logical-Z (single round)",
    )

    plt.plot(
        ps,
        pLX_ST,
        "o-",
        linewidth=2.5,
        label="Logical-X (space-time, k=3)",
    )

    plt.plot(
        ps,
        pLZ_ST,
        "s--",
        linewidth=2.5,
        label="Logical-Z (space-time, k=3)",
    )

    plt.xlabel(
        "Physical 1q depolarising probability $p_1$",
    )

    plt.ylabel(
        "Estimated logical failure rate",
    )

    plt.title(
        "Single-Round vs. Space-Time MWPM Decoding",
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    save_figure(save_path)

    plt.close()


def plot_lattice_comparison(
    x,
    y,
    xlabel,
    ylabel,
    title,
    save_path,
) -> None:
    """
    Compare benchmark results for rotated versus 
    unrotated Stim implementations.
    """

    plt.figure(figsize=(6, 4))

    for label, values in y.items():

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2,
            label=label,
        )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel(xlabel)

    plt.ylabel(ylabel)

    plt.title(title)

    plt.grid(
        which="both",
        alpha=0.3,
    )

    plt.legend()

    plt.tight_layout()

    save_figure(save_path)

    plt.close()


def plot_backend_comparison(
    physical_error_rates,
    stim_unrotated_rates,
    checkerboard_rates,
    distance: int,
    basis: str,
    save_path: str | Path | None = None,
) -> None:
    """
    Compare logical failure rates for the checkerboard
    reference implementation and Stim's canonical
    unrotated surface-code implementation.
    """

    plt.figure(figsize=(6, 4))

    plt.plot(
        physical_error_rates,
        stim_unrotated_rates,
        marker="o",
        linewidth=2,
        label="Stim (unrotated)",
    )

    plt.plot(
        physical_error_rates,
        checkerboard_rates,
        marker="s",
        linestyle="--",
        linewidth=2,
        label="Reference (checkerboard)",
    )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Physical error rate")
    plt.ylabel("Logical failure rate")

    plt.title(
        "Stim vs. Checkerboard "
        f"({basis} Memory, d={distance})"
    )

    plt.grid(
        which="both",
        alpha=0.3,
    )

    plt.legend()

    plt.tight_layout()

    save_figure(save_path)

    plt.close()