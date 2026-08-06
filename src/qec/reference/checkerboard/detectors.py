"""
Detector and logical-observable construction for the
checkerboard surface-code implementation.
"""

import stim


class DetectorMixin:
    """
    Detector and logical-observable construction routines.
    """

    def add_round_detectors(
        self,
        circuit: stim.Circuit,
        round_idx: int,
        current_record_idx: int,
    ) -> None:
        """
        Construct detector events between consecutive
        syndrome-extraction rounds.
        """

        if round_idx == 0:
            return

        for stabilizer_idx in range(
            self.n_stabilizers
        ):

            prev = self.get_measurement(
                round_idx - 1,
                stabilizer_idx,
            )

            curr = self.get_measurement(
                round_idx,
                stabilizer_idx,
            )

            stabilizer = self.stabilizers[
                stabilizer_idx
            ]

            x, y = (
                stabilizer.ancilla_position
            )

            basis = (
                0.0
                if stabilizer.stabilizer_type == "X"
                else 1.0
            )

            circuit.append(
                "DETECTOR",
                [
                    stim.target_rec(
                        self.rec_offset(
                            prev,
                            current_record_idx,
                        )
                    ),
                    stim.target_rec(
                        self.rec_offset(
                            curr,
                            current_record_idx,
                        )
                    ),
                ],
                [
                    x,
                    y,
                    float(round_idx),
                    basis,
                ],
            )

    def add_final_detectors(
        self,
        circuit: stim.Circuit,
        current_record_idx: int,
    ) -> None:
        """
        Add the final detector layer for a logical
        memory experiment.
        """

        last_round = self.rounds - 1

        stabilizer_type = self.memory_basis

        basis_coord = (
            0.0
            if stabilizer_type == "X"
            else 1.0
        )

        for stabilizer_idx in range(
            self.n_stabilizers
        ):

            stabilizer = self.stabilizers[
                stabilizer_idx
            ]

            if (
                stabilizer.stabilizer_type
                != stabilizer_type
            ):
                continue

            coordinates = (
                stabilizer.data_coordinates
            )

            syndrome_record = self.get_measurement(
                last_round,
                stabilizer_idx,
            )

            targets = [
                stim.target_rec(
                    self.rec_offset(
                        syndrome_record,
                        current_record_idx,
                    )
                )
            ]

            for r, c in coordinates:

                data_qubit = self.data_idx(
                    r,
                    c,
                )

                data_record = (
                    self.data_measurement_records[
                        data_qubit
                    ]
                )

                targets.append(
                    stim.target_rec(
                        self.rec_offset_from_record(
                            data_record,
                            current_record_idx,
                        )
                    )
                )

            x, y = (
                stabilizer.ancilla_position
            )

            circuit.append(
                "DETECTOR",
                targets,
                [
                    x,
                    y,
                    float(self.rounds),
                    basis_coord,
                ],
            )

    def logical_z_chain(self) -> list[int]:
        """
        Data qubits forming the logical Z operator.
        """

        return [
            self.data_idx(r, 0)
            for r in range(self.distance)
        ]

    def logical_x_chain(self) -> list[int]:
        """
        Data qubits forming the logical X operator.
        """

        return [
            self.data_idx(0, c)
            for c in range(self.distance)
        ]

    def add_logical_z_observable(
        self,
        circuit: stim.Circuit,
        current_record_idx: int,
    ) -> None:

        targets: list[stim.GateTarget] = []

        for q in self.logical_z_chain():

            record_idx = (
                self.data_measurement_records[q]
            )

            targets.append(
                stim.target_rec(
                    self.rec_offset_from_record(
                        record_idx,
                        current_record_idx,
                    )
                )
            )

        circuit.append(
            "OBSERVABLE_INCLUDE",
            targets,
            0,
        )

    def add_logical_x_observable(
        self,
        circuit: stim.Circuit,
        current_record_idx: int,
    ) -> None:

        targets: list[stim.GateTarget] = []

        for q in self.logical_x_chain():

            record_idx = (
                self.data_measurement_records[q]
            )

            targets.append(
                stim.target_rec(
                    self.rec_offset_from_record(
                        record_idx,
                        current_record_idx,
                    )
                )
            )

        circuit.append(
            "OBSERVABLE_INCLUDE",
            targets,
            0,
        )