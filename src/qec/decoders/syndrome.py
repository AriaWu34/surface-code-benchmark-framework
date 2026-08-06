"""
Utilities for processing syndrome measurement outcomes.

This module converts stabilizer measurement results into
detector events and space-time defects used by MWPM
decoders.
"""

import numpy as np

from qec.geometry import code_sizes


def split_into_rounds(
    bitstr: str,
    k: int,
    n_stabilizers: int,
) -> list[str]:
    """
    Split a syndrome measurement string into consecutive rounds.
    """
    s = bitstr.replace(" ", "")[::-1]

    return [
        s[i * n_stabilizers:(i + 1) * n_stabilizers]
        for i in range(k)
    ]


def parse_round_bits(
    round_bits: str,
    n_x: int,
) -> tuple[str, str]:
    """
    Split a syndrome round into X- and Z-stabilizer outcomes.
    """
    return round_bits[:n_x], round_bits[n_x:]


def defects_from_bits(bits: str) -> list[int]:
    """
    Return the indices of stabilizers detecting a syndrome event.
    """
    return [i for i, b in enumerate(bits) if b == "1"]


def spacetime_defects(
    full_bitstr: str,
    distance: int,
    k: int,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """
    Construct space-time syndrome defects for MWPM decoding.

    Successive syndrome rounds are compared to identify
    changes in stabilizer outcomes, which correspond to
    detector events in space-time.
    """
    
    _, n_x, n_z = code_sizes(distance)

    n_stabilizers = n_x + n_z

    rounds = split_into_rounds(
        full_bitstr,
        k,
        n_stabilizers,
    )

    syn = np.array(
        [
            [int(b) for b in rb]
            for rb in rounds
        ]
    )

    defects_z = []
    defects_x = []

    for t in range(k - 1):

        # Z stabilizer changes
        diff_z = syn[t, n_x:] != syn[t + 1, n_x:]

        for i, changed in enumerate(diff_z):
            if changed:
                defects_z.append((i, t))

        # X stabilizer changes
        diff_x = syn[t, :n_x] != syn[t + 1, :n_x]

        for i, changed in enumerate(diff_x):
            if changed:
                defects_x.append((i, t))

    return defects_z, defects_x