"""
Helper utilities and measurement bookkeeping for the
checkerboard surface-code implementation.
"""

from dataclasses import dataclass

from qec.geometry import d_idx


@dataclass(frozen=True)
class StabilizerMeasurement:
    """
    Metadata describing a stabilizer measurement.
    """

    round_idx: int
    stabilizer_idx: int
    record_idx: int


class HelperMixin:
    """
    Measurement bookkeeping and helper utilities.
    """

    def reset_measurements(self) -> None:
        """
        Clear measurement bookkeeping.
        """

        self.measurements.clear()
        self.data_measurement_records.clear()

    def record_measurement(
        self,
        round_idx: int,
        stabilizer_idx: int,
        record_idx: int,
    ) -> None:
        """
        Store stabilizer measurement metadata.
        """

        self.measurements[
            (round_idx, stabilizer_idx)
        ] = StabilizerMeasurement(
            round_idx=round_idx,
            stabilizer_idx=stabilizer_idx,
            record_idx=record_idx,
        )

    def get_measurement(
        self,
        round_idx: int,
        stabilizer_idx: int,
    ) -> StabilizerMeasurement:
        """
        Retrieve a recorded stabilizer measurement.
        """

        return self.measurements[
            (round_idx, stabilizer_idx)
        ]

    def data_idx(
        self,
        row: int,
        col: int,
    ) -> int:
        """
        Return the linear index of a data qubit.
        """

        return d_idx(
            row,
            col,
            self.distance,
        )

    def rec_offset(
        self,
        measurement: StabilizerMeasurement,
        current_record_idx: int,
    ) -> int:
        """
        Convert an absolute record index into
        a Stim REC offset.
        """

        return (
            measurement.record_idx
            - current_record_idx
            - 1
        )

    def rec_offset_from_record(
        self,
        record_idx: int,
        current_record_idx: int,
    ) -> int:
        """
        Convert a raw measurement record index
        into a Stim REC offset.
        """

        return (
            record_idx
            - current_record_idx
            - 1
        )