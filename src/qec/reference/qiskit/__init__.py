"""
Qiskit reference backend.

Exports the lightweight Qiskit implementation used
for reference simulations and decoder comparisons.
"""

from .backend import QiskitBackend

__all__ = [
    "QiskitBackend",
]