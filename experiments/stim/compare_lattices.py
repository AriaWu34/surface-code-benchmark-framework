"""
Compare rotated and unrotated Stim surface codes.

Usage:
    python experiments/stim/compare_lattices.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from qec.analysis.io import (
    load_dataframe,
    save_dataframe,
    should_rerun,
)
from qec.backends.stim import StimBackend
from qec.visualization import plot_lattice_comparison


OUTPUT_DIR = Path(
    "results/stim/compare_lattices"
)

#
# Experiment configuration
#

USE_CACHE = True

DISTANCES = (
    3,
    5,
    7,
)

PHYSICAL_ERROR_RATES = np.array([
    0.0005,
    0.0010,
    0.0015,
    0.0020,
    0.0025,
    0.0030,
    0.0035,
    0.0040,
    0.0045,
    0.0050,
])

SHOTS = 50_000

LATTICES = (
    "rotated",
    "unrotated",
)

MEMORY_BASES = (
    "X",
    "Z",
)


def run_experiment(
    basis: str,
    distance: int,
) -> tuple[
    dict[str, np.ndarray],
    pd.DataFrame,
]:
    """
    Compare the logical failure rates of rotated and
    unrotated Stim surface codes.
    """

    comparison = {}

    rows = []

    for lattice in LATTICES:

        print(
            f"\nRunning {lattice}"
        )

        backend = StimBackend(
            lattice=lattice,
        )

        logical_rates = []

        for p in PHYSICAL_ERROR_RATES:

            logical = backend.logical_failure_rate(
                distance=distance,
                rounds=distance,
                shots=SHOTS,
                depolarizing_error=p,
                readout_error=p,
                memory_basis=basis,
            )

            logical_rates.append(
                logical
            )

            rows.append(
                {
                    "lattice": lattice,
                    "distance": distance,
                    "physical_error_rate": p,
                    "logical_error_rate": logical,
                }
            )

            print(
                f"{lattice:<10}"
                f"p={p:.4f} "
                f"logical={logical:.6e}"
            )

        comparison[lattice] = np.asarray(
            logical_rates
        )

    return (
        comparison,
        pd.DataFrame(rows),
    )


def main() -> None:

    for basis in MEMORY_BASES:

        basis_output_dir = (
            OUTPUT_DIR / basis
        )

        for distance in DISTANCES:

            print(
                f"\n=== {basis}-memory (d={distance}) ==="
            )

            csv_path = (
                basis_output_dir
                / f"d{distance}.csv"
            )

            if should_rerun(
                csv_path,
                use_cache=USE_CACHE,
            ):

                print(
                    "\nRunning Monte Carlo simulation..."
                )

                comparison, df = (
                    run_experiment(
                        basis,
                        distance,
                    )
                )

                save_dataframe(
                    df,
                    csv_path,
                )

            else:

                print(
                    f"\nLoading cached results: "
                    f"{csv_path}"
                )

                df = load_dataframe(
                    csv_path,
                )

                comparison = {}

                for (
                    lattice,
                    group,
                ) in (
                    df.groupby("lattice")
                ):

                    comparison[lattice] = (
                        group
                        .sort_values(
                            "physical_error_rate"
                        )[
                            "logical_error_rate"
                        ]
                        .to_numpy()
                    )

            plot_lattice_comparison(
                x=PHYSICAL_ERROR_RATES,
                y=comparison,
                xlabel="Physical error rate",
                ylabel="Logical failure rate",
                title=(
                    "Rotated vs. Unrotated Surface Codes\n"
                    f"{basis}-Memory (d={distance})"
                ),
                save_path=(
                    basis_output_dir
                    / f"d{distance}.png"
                ),
            )


if __name__ == "__main__":
    main()