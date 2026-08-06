"""
Abstract interface for quantum error-correction backends.
"""

from abc import ABC, abstractmethod


class Backend(ABC):
    """
    Abstract base class for surface-code simulation backends.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the backend name."""

    @abstractmethod
    def logical_failure_rate(self, *args, **kwargs):
        """
        Estimate the logical failure rate of a logical-memory
        experiment.
        """