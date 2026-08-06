"""
Checkerboard reference implementation.

Exports the checkerboard backend together with the
explicit first-principles surface-code model.
"""

from .backend import CheckerboardBackend
from .checkerboard_surface_code import CheckerboardSurfaceCode

__all__ = [
    "CheckerboardBackend",
    "CheckerboardSurfaceCode",
]