"""
Compare single-round and space-time decoding.

Usage:
    python experiments/reference/qiskit_decoder_strategy.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from qec.analysis.io import (
    load_dataframe,
    save_dataframe,
    should_rerun,
)
from qec.reference.qiskit.engine import (
    compare_single_vs_spacetime,
)
from qec.visualization import (
    plot_decoder_comparison,
)


OUTPUT_DIR = Path(
    "results/reference/qiskit_decoder_strategy"
)

#
# Experiment configuration
#

USE_CACHE = True

PHYSICAL_ERROR_RATES = np.array([
    0.005,
    0.010,
    0.015,
    0.020,
    0.030,
    0.040,
    0.050,
    0.060,
    0.080,
])

SHOTS = 10_000

K_SINGLE = 1

K_SPACETIME = 3

READOUT_ERROR = 0.01


def run_experiment() -> tuple[
    tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
    pd.DataFrame,
]:
    """
    Compare single-round and space-time MWPM decoding
    using the Qiskit reference backend.
    """

    (
        p_vals,
        logical_x_single,
        logical_z_single,
        logical_x_spacetime,
        logical_z_spacetime,
    ) = compare_single_vs_spacetime(
        PHYSICAL_ERROR_RATES,
        k_space_time=K_SPACETIME,
        k_single=K_SINGLE,
        shots=SHOTS,
        ro=READOUT_ERROR,
    )

    df = pd.DataFrame(
        {
            "physical_error_rate": p_vals,
            "logical_x_single": logical_x_single,
            "logical_z_single": logical_z_single,
            "logical_x_spacetime": logical_x_spacetime,
            "logical_z_spacetime": logical_z_spacetime,
        }
    )

    return (
        (
            p_vals,
            logical_x_single,
            logical_z_single,
            logical_x_spacetime,
            logical_z_spacetime,
        ),
        df,
    )


def main() -> None:

    csv_path = (
        OUTPUT_DIR
        / "results.csv"
    )

    if should_rerun(
        csv_path,
        use_cache=USE_CACHE,
    ):

        print(
            "Running decoder strategy experiment..."
        )

        results, df = run_experiment()

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

        results = (
            df[
                "physical_error_rate"
            ].to_numpy(),
            df[
                "logical_x_single"
            ].to_numpy(),
            df[
                "logical_z_single"
            ].to_numpy(),
            df[
                "logical_x_spacetime"
            ].to_numpy(),
            df[
                "logical_z_spacetime"
            ].to_numpy(),
        )

    plot_decoder_comparison(
        *results,
        save_path=(
            OUTPUT_DIR
            / "decoder_strategy.png"
        ),
    )


if __name__ == "__main__":
    main()