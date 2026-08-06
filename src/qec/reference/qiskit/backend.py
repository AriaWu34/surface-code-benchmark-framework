"""
High-level interface for the Qiskit reference backend.

This module provides the public API for running logical
failure-rate simulations using the lightweight Qiskit-based
surface-code implementation.
"""

from qec.backends.base import Backend
from .engine import (
    logical_failure_rates_single,
    logical_failure_rates_spacetime,
)


class QiskitBackend(Backend):
    """
    High-level interface for the Qiskit reference
    surface-code backend.
    """

    @property
    def name(self) -> str:
        """Return the backend identifier."""
        return "qiskit"

    def logical_failure_rate(self, *args, **kwargs):
        """
        Estimate the logical failure rate of a Qiskit
        surface-code memory experiment using single-round
        MWPM decoding.
        """
        return logical_failure_rates_single(
            *args,
            **kwargs,
        )

    def logical_failure_rate_spacetime(
        self,
        *args,
        **kwargs,
    ):
        """
        Estimate the logical failure rate of a Qiskit
        surface-code memory experiment using space-time
        MWPM decoding.
        """
        return logical_failure_rates_spacetime(
            *args,
            **kwargs,
        )