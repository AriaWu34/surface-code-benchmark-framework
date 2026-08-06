import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from qec.visualization.common import save_figure
from qec.visualization.comparison import (
    plot_backend_comparison,
    plot_decoder_comparison,
    plot_lattice_comparison,
)
from qec.visualization.logical_failure import (
    plot_distance_scaling,
    plot_logical_failure_rate,
)
from qec.visualization.runtime import (
    plot_runtime_scaling,
)
from qec.visualization.threshold import (
    plot_threshold,
)


def assert_saved(path: Path) -> None:

    try:
        assert path.exists()
        assert path.stat().st_size > 0
    finally:
        plt.close("all")


def test_save_figure(tmp_path):

    plt.figure()

    plt.plot([0, 1], [0, 1])

    path = tmp_path / "figure.png"

    save_figure(path)

    assert_saved(path)


def test_plot_logical_failure_rate(tmp_path):

    path = tmp_path / "logical.png"

    plot_logical_failure_rate(
        physical_error_rates=np.array(
            [0.001, 0.002, 0.003]
        ),
        logical_error_rates=np.array(
            [0.01, 0.02, 0.03]
        ),
        lattice="rotated",
        basis="X",
        distance=3,
        save_path=path,
    )

    assert_saved(path)


def test_plot_distance_scaling(tmp_path):

    path = tmp_path / "distance.png"

    plot_distance_scaling(
        physical_error_rates=np.array(
            [0.001, 0.002, 0.003]
        ),
        logical_error_rates_by_distance={
            3: np.array(
                [0.03, 0.02, 0.01]
            ),
            5: np.array(
                [0.02, 0.01, 0.005]
            ),
        },
        lattice="rotated",
        basis="X",
        save_path=path,
    )

    assert_saved(path)


def test_plot_threshold(tmp_path):

    path = tmp_path / "threshold.png"

    plot_threshold(
        physical_error_rates=np.array(
            [0.001, 0.002, 0.003]
        ),
        logical_error_rates_by_distance={
            3: np.array(
                [0.03, 0.02, 0.01]
            ),
            5: np.array(
                [0.02, 0.01, 0.005]
            ),
        },
        lattice="rotated",
        basis="Z",
        threshold=0.002,
        save_path=path,
    )

    assert_saved(path)


def test_plot_runtime_scaling(tmp_path):

    path = tmp_path / "runtime.png"

    plot_runtime_scaling(
        distances=[3, 5, 7],
        runtimes={
            "rotated": {
                "mean": [0.2, 0.5, 1.1],
                "std": [0.01, 0.02, 0.05],
            },
            "unrotated": {
                "mean": [0.3, 0.7, 1.5],
                "std": [0.02, 0.03, 0.06],
            },
        },
        save_path=path,
    )

    assert_saved(path)


def test_plot_lattice_comparison(tmp_path):

    path = tmp_path / "lattice.png"

    x = np.array(
        [0.001, 0.002, 0.003]
    )

    plot_lattice_comparison(
        x=x,
        y={
            "rotated": [0.01, 0.02, 0.03],
            "unrotated": [0.015, 0.025, 0.04],
        },
        xlabel="Physical error rate",
        ylabel="Logical failure rate",
        title="Comparison",
        save_path=path,
    )

    assert_saved(path)


def test_plot_backend_comparison(tmp_path):

    path = tmp_path / "backend.png"

    x = np.array(
        [0.001, 0.002, 0.003]
    )

    plot_backend_comparison(
        physical_error_rates=x,
        stim_unrotated_rates=[0.01, 0.02, 0.03],
        checkerboard_rates=[0.015, 0.025, 0.04],
        distance=3,
        basis="Z",
        save_path=path,
    )

    assert_saved(path)


def test_plot_decoder_comparison(tmp_path):

    path = tmp_path / "decoder.png"

    x = np.array(
        [0.0, 0.02, 0.04]
    )

    plot_decoder_comparison(
        x,
        [0.01, 0.02, 0.03],
        [0.02, 0.03, 0.04],
        [0.005, 0.01, 0.015],
        [0.01, 0.015, 0.02],
        save_path=path,
    )

    assert_saved(path)