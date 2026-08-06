"""
Logical failure-rate experiment using the Stim backend.

Usage:
    python experiments/stim/distance_scaling.py
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
from qec.visualization import (
    plot_distance_scaling,
    plot_logical_failure_rate,
)


OUTPUT_DIR = Path(
    "results/stim/distance_scaling"
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
    backend: StimBackend,
    basis: str,
) -> tuple[
    dict[int, np.ndarray],
    pd.DataFrame,
]:
    """
    Run logical-memory simulations for one lattice.
    """

    results = {}

    rows = []

    for distance in DISTANCES:

        print(
            f"\nRunning d={distance}"
        )

        logical_rates = []

        for p in PHYSICAL_ERROR_RATES:

            logical = (
                backend.logical_failure_rate(
                    distance=distance,
                    rounds=distance,
                    shots=SHOTS,
                    depolarizing_error=p,
                    readout_error=p,
                    memory_basis=basis,
                )
            )

            logical_rates.append(
                logical
            )

            rows.append(
                {
                    "distance": distance,
                    "physical_error_rate": p,
                    "logical_error_rate": logical,
                }
            )

            print(
                f"d={distance:<2} "
                f"p={p:.4f} "
                f"logical={logical:.6e}"
            )

        results[distance] = np.asarray(
            logical_rates
        )

    return (
        results,
        pd.DataFrame(rows),
    )


def main() -> None:

    for lattice in LATTICES:

        backend = StimBackend(
            lattice=lattice,
        )

        for basis in MEMORY_BASES:

            print(
                f"\n=== "
                f"{lattice.capitalize()} "
                f"{basis}-memory ==="
            )

            output_dir = (
                OUTPUT_DIR
                / lattice
                / basis
            )

            csv_path = (
                output_dir
                / "logical_failure_rates.csv"
            )

            if should_rerun(
                csv_path,
                use_cache=USE_CACHE,
            ):

                print(
                    "\nRunning Monte Carlo simulation..."
                )

                (
                    results,
                    df,
                ) = run_experiment(
                    backend,
                    basis,
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

                results = {}

                for (
                    distance,
                    group,
                ) in (
                    df.groupby("distance")
                ):

                    results[
                        int(distance)
                    ] = (
                        group
                        .sort_values(
                            "physical_error_rate"
                        )[
                            "logical_error_rate"
                        ]
                        .to_numpy()
                    )

            #
            # Individual curves
            #

            for (
                distance,
                logical_rates,
            ) in results.items():

                plot_logical_failure_rate(
                    physical_error_rates=PHYSICAL_ERROR_RATES,
                    logical_error_rates=logical_rates,
                    distance=distance,
                    save_path=(
                        output_dir
                        / f"d{distance}.png"
                    ),
                )

            #
            # Distance scaling
            #

            plot_distance_scaling(
                physical_error_rates=PHYSICAL_ERROR_RATES,
                logical_error_rates_by_distance=results,
                save_path=(
                    output_dir
                    / "distance_scaling.png"
                ),
            )


if __name__ == "__main__":
    main()