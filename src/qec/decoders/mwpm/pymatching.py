"""
PyMatching implementation of the Minimum Weight
Perfect Matching (MWPM) decoder.

This module provides a common decoder interface
used by the Stim backend.

It supports:

- PyMatching decoding of Stim detector error models.
- Delegation to the reference NetworkX decoder
  for simulations.
"""

import pymatching

from qec.decoders.base import Decoder

from .networkx import (
    decode_one_shot,
)


class MWPMDecoder(Decoder):
    """
    Common interface to MWPM decoder implementations.

    Provides a common interface to the reference
    NetworkX implementation and the PyMatching decoder
    used by the framework.
    """

    def __init__(
        self,
        implementation: str = "networkx",
        dem=None,
    ):
        """
        Create an MWPM decoder.

        Parameters
        ----------
        implementation
            Decoder implementation ("networkx" or "pymatching").

        dem
            Stim detector error model required by the
            PyMatching implementation.
        """

        self.implementation = implementation

        self.matching = None

        if implementation == "pymatching":

            if dem is None:
                raise ValueError(
                    "DEM required for "
                    "PyMatching implementation."
                )

            self.matching = (
                pymatching.Matching
                .from_detector_error_model(
                    dem
                )
            )

        elif implementation != "networkx":
            raise ValueError(
                f"Unknown implementation: "
                f"{implementation}"
            )


    def decode(
        self,
        bitstr: str,
        distance: int,
        k: int = 1,
    ) -> tuple[int, int]:
        """
        Decode detector events using the selected MWPM
        implementation.
        """
        return decode_one_shot(
            bitstr=bitstr,
            distance=distance,
            k=k,
        )
    
    def decode_detection_events(
        self,
        detection_events,
    ):
        """
        Decode detector events using
        the PyMatching implementation.
        """

        if self.implementation != "pymatching":
            raise ValueError(
                "PyMatching implementation required."
            )

        return self.matching.decode(
            detection_events
        )