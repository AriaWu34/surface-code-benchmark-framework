"""
Circuit construction routines for the checkerboard
surface-code reference implementation.

This module contains the low-level routines used to
construct stabilizer measurements, syndrome
extraction rounds, logical-state preparation, and
physical noise.
"""

import stim


class CircuitMixin:
    """
    Circuit-building routines for the checkerboard
    surface-code implementation.
    """

    def prepare_logical_state(
        self,
        circuit: stim.Circuit,
    ):
        """
        Prepare the initial logical memory state.
        """

        if self.memory_basis == "Z":
            return

        if self.memory_basis == "X":
            circuit.append(
                "H",
                self.data_indices,
            )

    def add_x_stabilizer(
        self,
        circuit: stim.Circuit,
        ancilla: int,
        coordinates: tuple[
            tuple[int, int],
            ...
        ],
    ) -> None:
        """
        Add an X-stabilizer measurement.
        """

        circuit.append("H", [ancilla])

        for row, col in coordinates:
            circuit.append(
                "CX",
                [
                    ancilla,
                    self.data_idx(row, col),
                ],
            )

        circuit.append("H", [ancilla])

        self.add_readout_error(
            circuit,
            ancilla,
        )

        circuit.append(
            "M",
            [ancilla],
        )

    def add_z_stabilizer(
        self,
        circuit: stim.Circuit,
        ancilla: int,
        coordinates: tuple[
            tuple[int, int],
            ...
        ],
    ) -> None:
        """
        Add a Z-stabilizer measurement.
        """

        for row, col in coordinates:
            circuit.append(
                "CX",
                [
                    self.data_idx(row, col),
                    ancilla,
                ],
            )

        self.add_readout_error(
            circuit,
            ancilla,
        )

        circuit.append(
            "M",
            [ancilla],
        )

    def add_syndrome_round(
        self,
        circuit: stim.Circuit,
        round_idx: int,
        record_idx: int,
    ) -> int:
        """
        Add a single syndrome-extraction round.
        """

        circuit.append(
            "R",
            self.ancilla_indices,
        )

        for stabilizer in self.stabilizers:

            ancilla = (
                self.stabilizer_ancilla_start
                + stabilizer.stabilizer_idx
            )

            coordinates = (
                stabilizer.data_coordinates
            )

            if stabilizer.stabilizer_type == "X":

                self.add_x_stabilizer(
                    circuit,
                    ancilla,
                    coordinates,
                )

            else:

                self.add_z_stabilizer(
                    circuit,
                    ancilla,
                    coordinates,
                )

            self.record_measurement(
                round_idx=round_idx,
                stabilizer_idx=(
                    stabilizer.stabilizer_idx
                ),
                record_idx=record_idx,
            )

            record_idx += 1

        self.add_depolarizing_noise(
            circuit,
            self.data_indices,
        )

        return record_idx
    
    def measure_data_qubits(
        self,
        circuit: stim.Circuit,
    ):
        """
        Measure data qubits in the memory basis.
        """

        if self.memory_basis == "Z":

            circuit.append(
                "M",
                self.data_indices,
            )

        elif self.memory_basis == "X":

            circuit.append(
                "H",
                self.data_indices,
            )

            circuit.append(
                "M",
                self.data_indices,
            )

    def add_final_data_measurements(
        self,
        circuit: stim.Circuit,
        record_idx: int,
    ) -> int:
        """
        Measure all data qubits and record their
        measurement indices.
        """

        if self.readout_error > 0:
            circuit.append(
                "X_ERROR",
                self.data_indices,
                self.readout_error,
            )

        self.measure_data_qubits(
            circuit
        )

        for q in self.data_indices:
            self.data_measurement_records[q] = record_idx
            record_idx += 1

        return record_idx

    def add_depolarizing_noise(
        self,
        circuit: stim.Circuit,
        qubits,
    ) -> None:
        """
        Apply single-qubit depolarizing noise.
        """

        if self.depolarizing_error == 0:
            return

        circuit.append(
            "DEPOLARIZE1",
            qubits,
            self.depolarizing_error,
        )

    def add_readout_error(
        self,
        circuit: stim.Circuit,
        qubit: int,
    ) -> None:
        """
        Apply measurement error immediately before
        a measurement operation.
        """

        if self.readout_error == 0:
            return

        circuit.append(
            "X_ERROR",
            [qubit],
            self.readout_error,
        )