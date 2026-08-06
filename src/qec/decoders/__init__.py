"""
Decoder implementations for quantum error correction.

The package currently provides Minimum Weight Perfect
Matching (MWPM) decoders through a common interface.
"""

from .mwpm.pymatching import MWPMDecoder

__all__ = [
    "MWPMDecoder",
]