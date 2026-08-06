import numpy as np

from qec.reference.qiskit import engine
from qec.reference.qiskit.engine import (
    logical_failure_rates_single,
    logical_failure_rates_spacetime,
)


def test_single_round_engine_runs():
    fx, fz = logical_failure_rates_single(
        distance=3,
        shots=10,
    )

    assert 0.0 <= fx <= 1.0
    assert 0.0 <= fz <= 1.0


def test_spacetime_engine_runs():

    fx, fz = logical_failure_rates_spacetime(
        distance=3,
        shots=10,
    )

    assert 0.0 <= fx <= 1.0
    assert 0.0 <= fz <= 1.0


def test_compare_single_vs_spacetime(monkeypatch):

    def fake_single(**kwargs):
        return 0.1, 0.2

    def fake_spacetime(**kwargs):
        return 0.05, 0.08

    monkeypatch.setattr(
        engine,
        "logical_failure_rates_single",
        fake_single,
    )

    monkeypatch.setattr(
        engine,
        "logical_failure_rates_spacetime",
        fake_spacetime,
    )

    p = np.array(
        [0.001, 0.002]
    )

    (
        p_out,
        lx_single,
        lz_single,
        lx_space,
        lz_space,
    ) = engine.compare_single_vs_spacetime(
        p,
    )

    np.testing.assert_array_equal(
        p_out,
        p,
    )

    assert np.all(
        lx_single == 0.1
    )

    assert np.all(
        lz_single == 0.2
    )

    assert np.all(
        lx_space == 0.05
    )

    assert np.all(
        lz_space == 0.08
    )


def test_compare_passes_parameters(monkeypatch):

    calls = []

    def fake_single(**kwargs):

        calls.append(
            ("single", kwargs)
        )

        return 0.0, 0.0

    def fake_space(**kwargs):

        calls.append(
            ("space", kwargs)
        )

        return 0.0, 0.0

    monkeypatch.setattr(
        engine,
        "logical_failure_rates_single",
        fake_single,
    )

    monkeypatch.setattr(
        engine,
        "logical_failure_rates_spacetime",
        fake_space,
    )

    engine.compare_single_vs_spacetime(
        [0.005],
        k_single=1,
        k_space_time=3,
        shots=123,
        ro=0.02,
        distance=5,
    )

    assert calls[0][1]["distance"] == 5
    assert calls[0][1]["shots"] == 123
    assert calls[0][1]["p1"] == 0.005

    assert calls[1][1]["distance"] == 5
    assert calls[1][1]["shots"] == 123
    assert calls[1][1]["p1"] == 0.005