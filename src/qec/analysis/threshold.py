"""
Threshold estimation utilities.

Provides routines for estimating surface-code
thresholds from logical failure-rate curves together
with utilities for summarising and exporting the
results.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


THRESHOLD_SEARCH_REGION = (
    0.005,
    0.012,
)


@dataclass(slots=True)
class ThresholdEstimate:
    """
    Result of a threshold estimation.

    Stores the estimated threshold together with all
    pairwise curve crossings and summary statistics.
    """

    threshold: float | None

    pairwise_crossings: dict[
        tuple[int, int],
        float | None,
    ]

    mean: float | None

    std: float | None

    def to_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Convert the threshold estimate into a
        single-row DataFrame.
        """

        data = {
            "threshold": self.threshold,
            "mean": self.mean,
            "std": self.std,
        }

        for (
            d1,
            d2,
        ), crossing in (
            self.pairwise_crossings.items()
        ):

            data[f"{d1}-{d2}"] = crossing

        return pd.DataFrame(
            [data]
        )


def estimate_crossing(
    physical_error_rates,
    curve1,
    curve2,
    search_region=THRESHOLD_SEARCH_REGION,
) -> float | None:
    """
    Estimate the crossing point of two logical-error
    curves using linear interpolation.

    Only crossings inside the search region are
    considered to avoid spurious crossings caused by
    Monte Carlo noise.
    """

    x = np.asarray(
        physical_error_rates,
        dtype=float,
    )

    y = (
        np.asarray(curve1, dtype=float)
        - np.asarray(curve2, dtype=float)
    )

    low, high = search_region

    crossings = []

    for i in range(len(x) - 1):

        if not (
            low <= x[i] <= high
            or low <= x[i + 1] <= high
        ):
            continue

        if y[i] == 0:

            crossings.append(
                float(x[i])
            )

            continue

        if y[i] * y[i + 1] < 0:

            crossing = (
                x[i]
                - y[i]
                * (x[i + 1] - x[i])
                / (y[i + 1] - y[i])
            )

            crossings.append(
                float(crossing)
            )

    if not crossings:
        return None

    centre = 0.5 * (low + high)

    return min(
        crossings,
        key=lambda c: abs(c - centre),
    )


def estimate_threshold(
    physical_error_rates,
    logical_error_rates_by_distance,
) -> ThresholdEstimate:
    """
    Estimate the logical-error threshold from pairwise
    crossings of neighbouring code-distance curves.
    """

    distances = sorted(
        logical_error_rates_by_distance
    )

    pairwise = {}

    crossings = []

    for d1, d2 in zip(
        distances[:-1],
        distances[1:],
    ):

        crossing = estimate_crossing(
            physical_error_rates,
            logical_error_rates_by_distance[d1],
            logical_error_rates_by_distance[d2],
        )

        pairwise[(d1, d2)] = crossing

        if crossing is not None:
            crossings.append(crossing)

    if crossings:

        mean = float(
            np.mean(crossings)
        )

        std = float(
            np.std(crossings)
        )

    else:

        mean = None
        std = None

    return ThresholdEstimate(
        threshold=mean,
        pairwise_crossings=pairwise,
        mean=mean,
        std=std,
    )


def summarize_threshold(
    estimate: ThresholdEstimate,
) -> str:
    """
    Generate a human-readable summary of a threshold
    estimation.
    """

    lines = [
        "Threshold estimation",
        "--------------------",
    ]

    if estimate.threshold is None:

        lines.append(
            "No threshold detected."
        )

    else:

        lines.append(
            f"Estimated threshold : "
            f"{100 * estimate.threshold:.2f}%"
        )

        lines.append(
            f"Pairwise σ          : "
            f"{100 * estimate.std:.2f}%"
        )

    lines.append("")
    lines.append(
        "Pairwise crossings"
    )

    for (
        d1,
        d2,
    ), crossing in (
        estimate.pairwise_crossings.items()
    ):

        value = (
            "None"
            if crossing is None
            else f"{100 * crossing:.2f}%"
        )

        lines.append(
            f"d={d1} ↔ d={d2} : {value}"
        )

    return "\n".join(lines)