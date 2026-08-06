"""
Visualization utilities for benchmark experiments.

Provides plotting functions for logical failure rates,
threshold estimation, runtime benchmarking, and
backend comparisons.
"""

from .logical_failure import (
    plot_logical_failure_rate,
    plot_distance_scaling,
)

from .comparison import (
    plot_decoder_comparison,
    plot_lattice_comparison,
    plot_backend_comparison,
)

from .threshold import (
    plot_threshold,
)

from .runtime import (
    plot_runtime_scaling,
)

__all__ = [
    "plot_logical_failure_rate",
    "plot_distance_scaling",
    "plot_decoder_comparison",
    "plot_lattice_comparison",
    "plot_backend_comparison",
    "plot_threshold",
    "plot_runtime_scaling",
]