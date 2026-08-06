"""
Abstract base class for decoder implementations.
"""

from abc import ABC, abstractmethod


class Decoder(ABC):
    """
    Abstract interface for syndrome decoders.

    Concrete decoder implementations translate syndrome
    information into predicted logical observables.
    """

    @abstractmethod
    def decode(self, *args, **kwargs):
        """
        Decode syndrome information and return the predicted
        logical observable or observables.
        """
        pass