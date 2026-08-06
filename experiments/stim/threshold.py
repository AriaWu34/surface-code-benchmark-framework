"""
Estimate the logical-error threshold of Stim surface codes.

Usage:
    python experiments/stim/threshold.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from qec.analysis.io import (
    save_dataframe,
    save_text,
    load_dataframe,
    should_rerun,
)
from qec.analysis.threshold import (
    estimate_threshold,
    summarize_threshold,
)
from qec.backends.stim import StimBackend
from qec.visualization import plot_threshold


USE_CACHE = True

OUTPUT_DIR = Path(
    "results/stim/threshold"
)

#
# Experiment configuration
#

DISTANCES = (
    3,
    5,
    7,
    9,
)

PHYSICAL_ERROR_RATES = np.array([
    0.0010,
    0.0015,
    0.0020,
    0.0030,
    0.0040,
    0.0050,
    0.0060,
    0.0065,
    0.0070,
    0.0075,
    0.0080,
    0.0085,
    0.0090,
    0.0095,
    0.0100,
    0.0125,
    0.0150,
    0.0200,
])

DEFAULT_SHOTS = 50_000

THRESHOLD_SHOTS = 75_000

THRESHOLD_REGION = (
    0.0060,
    0.0100,
)

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
    distances: tuple[int, ...],
    physical_error_rates: np.ndarray,
    memory_basis: str,
) -> dict[int, np.ndarray]:
    """
    Run logical-memory simulations for threshold
    estimation.
    """

    results = {}

    low, high = THRESHOLD_REGION

    for distance in distances:

        print(
            f"\n{memory_basis}-memory: d={distance}"
        )

        logical_rates = []

        for i, p in enumerate(
            physical_error_rates,
            start=1,
        ):

            shots = (
                THRESHOLD_SHOTS
                if low <= p <= high
                else DEFAULT_SHOTS
            )

            print(
                f"  [{i:02d}/{len(physical_error_rates)}] "
                f"p={p:.4f} "
                f"({shots:,} shots)"
            )

            logical_rates.append(

                backend.logical_failure_rate(
                    distance=distance,
                    rounds=distance,
                    shots=shots,
                    depolarizing_error=p,
                    readout_error=p,
                    memory_basis=memory_basis,
                )

            )

        results[distance] = np.asarray(
            logical_rates
        )

    return results


def main() -> None:

    for lattice in LATTICES:

        print(
            f"\n{'=' * 15} "
            f"{lattice.upper()} "
            f"{'=' * 15}"
        )

        backend = StimBackend(
            lattice=lattice,
        )

        for basis in MEMORY_BASES:

            print(
                f"\n### {basis}-memory ###"
            )

            csv_path = (
                OUTPUT_DIR
                / lattice
                / f"{basis}.csv"
            )

            if should_rerun(
                csv_path,
                use_cache=USE_CACHE,
            ):

                print(
                    "\nRunning Monte Carlo simulation..."
                )

                logical_rates = run_experiment(
                    backend=backend,
                    distances=DISTANCES,
                    physical_error_rates=PHYSICAL_ERROR_RATES,
                    memory_basis=basis,
                )

                rows = []

                for distance, rates in sorted(
                    logical_rates.items()
                ):

                    for p, logical in zip(
                        PHYSICAL_ERROR_RATES,
                        rates,
                    ):

                        rows.append(
                            {
                                "distance": distance,
                                "physical_error_rate": p,
                                "logical_error_rate": logical,
                            }
                        )

                save_dataframe(
                    pd.DataFrame(rows),
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

                logical_rates = {}

                for (
                    distance,
                    group,
                ) in df.groupby(
                    "distance"
                ):

                    logical_rates[
                        int(distance)
                    ] = (
                        group[
                            "logical_error_rate"
                        ]
                        .to_numpy()
                    )

            #
            # Threshold analysis
            #

            estimate = estimate_threshold(
                physical_error_rates=PHYSICAL_ERROR_RATES,
                logical_error_rates_by_distance=logical_rates,
            )

            print()

            print(
                summarize_threshold(
                    estimate,
                )
            )

            #
            # Save threshold analysis
            #

            save_dataframe(
                estimate.to_dataframe(),
                OUTPUT_DIR
                / lattice
                / f"{basis}_threshold.csv",
            )

            save_text(
                summarize_threshold(
                    estimate,
                ),
                OUTPUT_DIR
                / lattice
                / f"{basis}_summary.txt",
            )

            #
            # Plot results
            #

            plot_threshold(
                physical_error_rates=PHYSICAL_ERROR_RATES,
                logical_error_rates_by_distance=logical_rates,
                lattice=lattice,
                basis=basis,
                threshold=estimate.threshold,
                save_path=(
                    OUTPUT_DIR
                    / lattice
                    / f"{basis}.png"
                ),
            )


if __name__ == "__main__":
    main()