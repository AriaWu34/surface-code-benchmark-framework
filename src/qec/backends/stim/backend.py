"""
High-level interface for the Stim backend.

This module provides the public API for running
surface-code simulations using Stim for circuit
generation and detector sampling together with
PyMatching for Minimum Weight Perfect Matching
(MWPM) decoding.
"""

from qec.backends.base import Backend
from qec.backends.stim.rotated import (
    RotatedSurfaceCode,
)
from qec.backends.stim.unrotated import (
    UnrotatedSurfaceCode,
)
from qec.decoders import MWPMDecoder


class StimBackend(Backend):
    """
    High-level interface for Stim-based
    surface-code simulations.
    """

    def __init__(
        self,
        lattice: str = "rotated",
    ):
        """
        Create a Stim simulation backend.

        Parameters
        ----------
        lattice
            Surface-code lattice to simulate ("rotated" or
            "unrotated").
        """

        if lattice not in {
            "rotated",
            "unrotated",
        }:
            raise ValueError(
                "lattice must be 'rotated' or 'unrotated'."
            )

        self.lattice = lattice

    @property
    def name(self) -> str:
        """Return the backend identifier."""
        return f"stim-{self.lattice}"

    def build_surface_code(
        self,
        **kwargs,
    ):
        """
        Construct a Stim-generated surface-code memory
        experiment.
        """

        if self.lattice == "rotated":
            return RotatedSurfaceCode(
                **kwargs,
            )

        return UnrotatedSurfaceCode(
            **kwargs,
        )

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
        Estimate the logical failure rate of a logical-memory
        experiment using Monte Carlo simulation and Minimum
        Weight Perfect Matching (MWPM) decoding.
        """

        code = self.build_surface_code(
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

        dets, obs = (
            code.sample_detectors_and_observables(
                shots=shots,
            )
        )

        failures = 0

        for det, actual in zip(
            dets,
            obs,
        ):

            predicted = (
                decoder.decode_detection_events(
                    det
                )
            )

            if not (predicted == actual).all():
                failures += 1

        return failures / shots