"""
Geometry and indexing utilities for the surface code.

Shared by backends and decoders.
"""

    
from dataclasses import dataclass

# ======================================================
# Indexing
# ======================================================

def d_idx(r: int, c: int, distance: int) -> int:
    """
    Convert a 2D data-qubit coordinate into a linear index.
    """
    return distance * r + c


def code_sizes(distance: int) -> tuple[int, int, int]:
    """
    Return the number of data, X-ancilla, and Z-ancilla qubits.
    """
    n_data = distance**2
    n_x = (distance - 1) ** 2
    n_z = (distance - 1) ** 2

    return n_data, n_x, n_z


def ancilla_offsets(distance: int) -> tuple[int, int]:
    """
    Return the starting indices of X and Z ancillas.
    """
    n_data, n_x, _ = code_sizes(distance)

    x_start = n_data
    z_start = n_data + n_x

    return x_start, z_start


# ======================================================
# Geometry
# ======================================================

def manhattan(p: tuple, q: tuple) -> float:
    """
    Manhattan distance between two coordinates.
    """
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def code_boundaries(distance: int) -> dict[str, float]:
    """
    Return decoder boundary coordinates.
    """
    low = -0.5
    high = distance - 0.5

    return {
        "top": low,
        "bottom": high,
        "left": low,
        "right": high,
        "span": float(distance),
    }


# ======================================================
# Validation
# ======================================================

def validate_distance(distance: int):
    """
    Validate that the code distance is an
    odd integer greater than or equal to 3.
    """
    if distance < 3 or distance % 2 == 0:
        raise ValueError(
            "Distance must be an odd integer >= 3."
        )


# ======================================================
# Reference helpers
# ======================================================

def generate_plaquettes(distance: int) -> list[list[tuple[int, int]]]:
    """
    Generate all 2×2 plaquettes used by the
    Qiskit circuit construction.

    This helper is retained for compatibility with
    the reference Qiskit backend.
    """
    plaqs = []

    for r in range(distance - 1):
        for c in range(distance - 1):
            plaqs.append(
                [
                    (r, c),
                    (r, c + 1),
                    (r + 1, c),
                    (r + 1, c + 1),
                ]
            )

    return plaqs


def valid_data_coordinate(
    row: int,
    col: int,
    distance: int,
) -> bool:
    """
    Return whether a data-qubit coordinate lies within
    the surface-code lattice.
    """

    return (
        0 <= row < distance
        and 0 <= col < distance
    )


def stabilizer_data_coordinates(
    row: int,
    col: int,
    distance: int,
) -> tuple[tuple[int, int], ...]:
    """
    Return all data qubits neighbouring an
    ancilla centred at (row+0.5, col+0.5).
    """

    neighbours = []

    candidates = [
        (row, col),
        (row, col + 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]

    for r, c in candidates:

        if valid_data_coordinate(
            r,
            c,
            distance,
        ):
            neighbours.append((r, c))

    return tuple(neighbours)


@dataclass(frozen=True)
class StabilizerGeometry:
    """
    Metadata describing the geometry of a stabilizer in the surface-code lattice.
    """

    stabilizer_idx: int

    stabilizer_type: str

    ancilla_position: tuple[float, float]

    data_coordinates: tuple[
        tuple[int, int],
        ...
    ]

    data_qubits: tuple[int, ...]

    boundary: bool = False

    @property
    def weight(self) -> int:
        """
        Number of data qubits acted on by the stabilizer.
        """
        return len(self.data_qubits)
    

def generate_stabilizers(
    distance: int,
) -> list[StabilizerGeometry]:
    """
    Generate the stabilizer geometry.

    Returns
    -------
    list[StabilizerGeometry]
        Metadata describing every stabilizer,
        including its type, ancilla position,
        neighbouring data qubits, and index.
    """

    stabilizers: list[
        StabilizerGeometry
    ] = []

    idx = 0

    for r in range(distance - 1):

        for c in range(distance - 1):

            coordinates = stabilizer_data_coordinates(
                r,
                c,
                distance,
            )

            stabilizers.append(
                StabilizerGeometry(
                    stabilizer_idx=idx,

                    stabilizer_type=(
                        "X"
                        if (r + c) % 2 == 0
                        else "Z"
                    ),

                    ancilla_position=(
                        r + 0.5,
                        c + 0.5,
                    ),

                    data_coordinates=coordinates,

                    data_qubits=tuple(
                        d_idx(
                            rr,
                            cc,
                            distance,
                        )
                        for rr, cc in coordinates
                    ),

                    boundary=False,
                )
            )

            idx += 1

    return stabilizers