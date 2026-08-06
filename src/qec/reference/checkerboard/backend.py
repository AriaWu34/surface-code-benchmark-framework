"""
High-level interface for the reference surface-code backend.

This backend provides an explicit, first-principles implementation
of the surface-code memory experiment. Unlike the Stim backend,
which relies on Stim's built-in circuit generator, this backend
constructs syndrome-extraction circuits directly from an explicit
lattice description.

It is intended as a readable reference implementation for
experimentation, validation, and education.
"""

from qec.backends.base import Backend
from qec.decoders import MWPMDecoder

from .checkerboard_surface_code import CheckerboardSurfaceCode


class CheckerboardBackend(Backend):
    """
    High-level interface for the checkerboard reference
    backend.
    """

    @property
    def name(self) -> str:
        """Return the backend identifier."""
        return "reference"

    def logical_failure_rate(
        self,
        distance: int = 3,
        rounds: int = 5,
        shots: int = 1000,
        depolarizing_error: float = 0.01,
        readout_error: float = 0.01,
        memory_basis: str = "Z",
    ) -> float:
        """
        Estimate the logical failure rate of a
        checkerboard surface-code memory experiment.
        """

        code = CheckerboardSurfaceCode(
            distance=distance,
            rounds=rounds,
            depolarizing_error=depolarizing_error,
            readout_error=readout_error,
            memory_basis=memory_basis,
        )

        decoder = MWPMDecoder(
            implementation="pymatching",
            dem=code.detector_error_model(),
        )

        dets, obs = code.sample_detectors_and_observables(
            shots=shots,
        )

        failures = 0

        for det, actual in zip(dets, obs):

            predicted = decoder.decode_detection_events(det)

            if not (predicted == actual).all():
                failures += 1

        return failures / shots