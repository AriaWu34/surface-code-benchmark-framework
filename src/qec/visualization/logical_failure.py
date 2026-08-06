"""
Logical failure-rate visualisations.
"""

import matplotlib.pyplot as plt

from .common import save_figure


def plot_logical_failure_rate(
    physical_error_rates,
    logical_error_rates,
    lattice: str,
    basis: str,
    distance,
    save_path=None,
) -> None:
    """
    Plot logical failure rate as a function of physical
    error probability for a single code distance.
    """

    plt.figure(figsize=(7.5, 5.2))

    plt.plot(
        physical_error_rates,
        logical_error_rates,
        "o-",
        linewidth=2,
        label=f"d={distance}",
    )

    plt.xlabel(
        "Physical error rate",
    )

    plt.ylabel(
        "Logical failure rate",
    )

    plt.title(
        "Logical Failure Rate\n"
        f"{lattice.capitalize()} Surface Code "
        f"({basis}-Memory, d={distance})",
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    save_figure(save_path)

    plt.close()



def plot_distance_scaling(
    physical_error_rates,
    logical_error_rates_by_distance,
    lattice: str,
    basis: str,
    save_path=None,
) -> None:
    """
    Plot logical failure rate for multiple code
    distances.
    """

    plt.figure(figsize=(7.5, 5.2))

    for distance, rates in (
        logical_error_rates_by_distance.items()
    ):

        plt.plot(
            physical_error_rates,
            rates,
            "o-",
            label=f"d={distance}",
        )

    plt.xlabel(
        "Physical error rate",
    )

    plt.ylabel(
        "Logical failure rate",
    )

    plt.title(
        "Logical Failure-Rate Scaling\n"
        f"{lattice.capitalize()} Surface Code "
        f"({basis}-Memory)",
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    save_figure(save_path)

    plt.close()