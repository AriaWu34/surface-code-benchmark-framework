"""
Visualization utilities for benchmark experiments.

Provides plotting functions for logical failure rates,
threshold estimation, runtime benchmarking, and
backend comparisons.
"""

from .comparison import (
    plot_backend_comparison,
    plot_decoder_comparison,
    plot_lattice_comparison,
)
from .logical_failure import (
    plot_distance_scaling,
    plot_logical_failure_rate,
)
from .runtime import (
    plot_runtime_scaling,
)
from .threshold import (
    plot_threshold,
)

__all__ = [
    "plot_backend_comparison",
    "plot_decoder_comparison",
    "plot_distance_scaling",
    "plot_lattice_comparison",
    "plot_logical_failure_rate",
    "plot_runtime_scaling",
    "plot_threshold",
]