"""
Benchmark runtime scaling of Stim surface-code simulations.

Usage:
    python experiments/stim/runtime_benchmark.py
"""

from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from qec.analysis.io import (
    load_dataframe,
    save_dataframe,
    should_rerun,
)
from qec.backends.stim import StimBackend
from qec.visualization import (
    plot_runtime_scaling,
)

OUTPUT_DIR = Path(
    "results/stim/runtime_benchmark"
)

#
# Experiment configuration
#

USE_CACHE = True

DISTANCES = (
    3,
    5,
    7,
    9,
)

LATTICES = (
    "rotated",
    "unrotated",
)

MEMORY_BASIS = "Z"

PHYSICAL_ERROR_RATE = 0.005

SHOTS = 50_000

REPEATS = 5


def benchmark(
    backend: StimBackend,
    distance: int,
) -> tuple[
    float,
    float,
    float,
]:
    """
    Benchmark the runtime of a single simulation
    configuration.
    """

    timings = []

    logical = None

    #
    # Warm-up (not timed)
    #

    backend.logical_failure_rate(
        distance=3,
        rounds=3,
        shots=100,
        depolarizing_error=PHYSICAL_ERROR_RATE,
        readout_error=PHYSICAL_ERROR_RATE,
        memory_basis=MEMORY_BASIS,
    )

    for _ in range(REPEATS):

        start = perf_counter()

        logical = backend.logical_failure_rate(
            distance=distance,
            rounds=distance,
            shots=SHOTS,
            depolarizing_error=PHYSICAL_ERROR_RATE,
            readout_error=PHYSICAL_ERROR_RATE,
            memory_basis=MEMORY_BASIS,
        )

        timings.append(
            perf_counter() - start
        )

    return (
        float(np.mean(timings)),
        float(np.std(timings)),
        logical,
    )


def run_experiment() -> tuple[
    dict[str, dict[str, list[float]]],
    pd.DataFrame,
]:

    rows = []

    runtimes = {}

    for lattice in LATTICES:

        print(
            f"\n{lattice.capitalize()}"
        )

        backend = StimBackend(
            lattice=lattice,
        )

        mean_times = []

        std_times = []

        for distance in DISTANCES:

            print(
                f"Running d={distance}"
            )

            (
                mean_runtime,
                std_runtime,
                logical,
            ) = benchmark(
                backend,
                distance,
            )

            mean_times.append(
                mean_runtime
            )

            std_times.append(
                std_runtime
            )

            rows.append(
                {
                    "lattice": lattice,
                    "distance": distance,
                    "runtime_mean": mean_runtime,
                    "runtime_std": std_runtime,
                    "logical_failure_rate": logical,
                }
            )

            print(
                f"d={distance:<2}"
                f" runtime={mean_runtime:.3f}s"
                f" ± {std_runtime:.3f}s"
                f" logical={logical:.6e}"
            )

        runtimes[lattice] = {
            "mean": mean_times,
            "std": std_times,
        }

    return (
        runtimes,
        pd.DataFrame(rows),
    )


def main() -> None:

    csv_path = (
        OUTPUT_DIR
        / "runtime.csv"
    )

    if should_rerun(
        csv_path,
        use_cache=USE_CACHE,
    ):

        print(
            "Running runtime benchmark..."
        )

        runtimes, df = (
            run_experiment()
        )

        save_dataframe(
            df,
            csv_path,
        )

    else:

        print(
            f"Loading cached results: "
            f"{csv_path}"
        )

        df = load_dataframe(
            csv_path,
        )

        runtimes = {}

        for (
            lattice,
            group,
        ) in df.groupby(
            "lattice"
        ):

            group = group.sort_values(
                "distance"
            )

            runtimes[lattice] = {
                "mean": group[
                    "runtime_mean"
                ].to_numpy(),
                "std": group[
                    "runtime_std"
                ].to_numpy(),
            }

    plot_runtime_scaling(
        distances=DISTANCES,
        runtimes=runtimes,
        save_path=(
            OUTPUT_DIR
            / "runtime_scaling.png"
        ),
    )


if __name__ == "__main__":
    main()