import pytest
import stim

from qec.reference.checkerboard import CheckerboardSurfaceCode


def test_invalid_distance():
    with pytest.raises(ValueError):
        CheckerboardSurfaceCode(distance=4)


def test_invalid_rounds():
    with pytest.raises(ValueError):
        CheckerboardSurfaceCode(rounds=0)


def test_invalid_memory_basis():
    with pytest.raises(ValueError):
        CheckerboardSurfaceCode(memory_basis="Y")


def test_build_circuit():
    code = CheckerboardSurfaceCode()

    circuit = code.build_circuit()

    assert isinstance(circuit, stim.Circuit)


def test_detector_error_model():
    code = CheckerboardSurfaceCode()

    dem = code.detector_error_model()

    assert isinstance(
        dem,
        stim.DetectorErrorModel,
    )


def test_detector_sampler():
    code = CheckerboardSurfaceCode()

    sampler = code.compile_detector_sampler()

    assert sampler is not None


def test_sample_detectors():

    code = CheckerboardSurfaceCode()

    dets = code.sample_detectors(5)

    assert dets.shape[0] == 5


def test_sample_detectors_and_observables():

    code = CheckerboardSurfaceCode()

    dets, obs = code.sample_detectors_and_observables(
        5
    )

    assert dets.shape[0] == 5
    assert obs.shape[0] == 5