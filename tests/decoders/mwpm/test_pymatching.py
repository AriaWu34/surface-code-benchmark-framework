import pytest

from qec.backends.stim.rotated import RotatedSurfaceCode
from qec.decoders import MWPMDecoder


def test_invalid_implementation():

    with pytest.raises(ValueError):

        MWPMDecoder(
            implementation="bad",
        )


def test_pymatching_decoder_builds():

    code = RotatedSurfaceCode(
        distance=3,
        rounds=5,
        depolarizing_error=0.01,
    )

    decoder = MWPMDecoder(
        implementation="pymatching",
        dem=code.detector_error_model(),
    )

    assert decoder is not None


def test_pymatching_decode_runs():

    code = RotatedSurfaceCode(
        distance=3,
        rounds=5,
        depolarizing_error=0.01,
    )

    decoder = MWPMDecoder(
        implementation="pymatching",
        dem=code.detector_error_model(),
    )

    dets = code.sample_detectors(
        shots=1,
    )

    result = decoder.decode_detection_events(
        dets[0],
    )

    assert len(result) == 1