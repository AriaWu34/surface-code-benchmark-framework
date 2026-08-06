"""
Explicit first-principles implementation of a
checkerboard surface-code memory experiment.

The implementation explicitly constructs the qubit
layout, stabilizer measurements, syndrome
extraction, detector events, and logical
observables without relying on Stim's built-in
surface-code circuit generators.
"""

import stim

from qec.geometry import (
    code_sizes,
    generate_stabilizers,
    validate_distance,
)

from .helpers import HelperMixin
from .circuit import CircuitMixin
from .detectors import DetectorMixin


class CheckerboardSurfaceCode(
    HelperMixin,
    CircuitMixin,
    DetectorMixin,
):
    """
    Explicit first-principles implementation of a
    checkerboard surface-code memory experiment.
    """

    def __init__(
        self,
        distance: int = 3,
        rounds: int = 1,
        depolarizing_error: float = 0.0,
        readout_error: float = 0.0,
        memory_basis: str = "Z",
    ):
        """
        Create a checkerboard surface-code memory
        experiment.
        """

        validate_distance(distance)

        if rounds < 1:
            raise ValueError(
                "Rounds must be >= 1."
            )

        if memory_basis not in {"X", "Z"}:
            raise ValueError(
                "memory_basis must be 'X' or 'Z'."
            )

        self.memory_basis = memory_basis

        for p in (
            depolarizing_error,
            readout_error,
        ):
            if not 0.0 <= p <= 1.0:
                raise ValueError(
                    "Error probabilities must be in [0,1]."
                )

        self.distance = distance
        self.rounds = rounds
        self.depolarizing_error = depolarizing_error
        self.readout_error = readout_error

        self.stabilizers = (
            generate_stabilizers(
                distance
            )
        )

        (
            self.n_data,
            self.n_x,
            self.n_z,
        ) = code_sizes(distance)

        self.measurements = {}

        self.data_measurement_records = {}

    @property
    def n_qubits(self) -> int:
        return self.n_data + self.n_stabilizers

    @property
    def x_ancilla_start(self) -> int:
        return self.n_data

    @property
    def z_ancilla_start(self) -> int:
        return self.n_data + self.n_x

    @property
    def ancilla_indices(self) -> range:
        return range(
            self.n_data,
            self.n_qubits,
        )

    @property
    def data_indices(self) -> range:
        return range(self.n_data)

    @property
    def n_stabilizers(self) -> int:
        return len(self.stabilizers)

    @property
    def stabilizer_ancilla_start(self) -> int:
        return self.n_data

    def build_circuit(self) -> stim.Circuit:
        """
        Build a Stim surface-code circuit for a
        logical memory experiment.
        """

        self.reset_measurements()

        record_idx = 0

        circuit = stim.Circuit()

        circuit.append(
            "R",
            range(self.n_qubits),
        )

        self.prepare_logical_state(
            circuit
        )

        for round_idx in range(
            self.rounds
        ):

            record_idx = (
                self.add_syndrome_round(
                    circuit,
                    round_idx,
                    record_idx,
                )
            )

            self.add_round_detectors(
                circuit,
                round_idx,
                record_idx - 1,
            )

        record_idx = (
            self.add_final_data_measurements(
                circuit,
                record_idx,
            )
        )

        self.add_final_detectors(
            circuit,
            record_idx - 1,
        )

        if self.memory_basis == "Z":

            self.add_logical_z_observable(
                circuit,
                record_idx - 1,
            )

        else:

            self.add_logical_x_observable(
                circuit,
                record_idx - 1,
            )

        return circuit

    def detector_error_model(
        self,
    ) -> stim.DetectorErrorModel:
        """
        Generate the detector error model.
        """

        return (
            self.build_circuit()
            .detector_error_model()
        )

    def compile_detector_sampler(
        self,
    ) -> stim.CompiledDetectorSampler:
        """
        Compile a detector sampler.
        """

        return (
            self.build_circuit()
            .compile_detector_sampler()
        )

    def sample_detectors(
        self,
        shots: int,
    ):
        """
        Sample detector outcomes.
        """

        return (
            self.compile_detector_sampler()
            .sample(shots)
        )

    def sample_detectors_and_observables(
        self,
        shots: int,
    ):
        """
        Sample detector outcomes and logical
        observables.
        """

        return (
            self.build_circuit()
            .compile_detector_sampler()
            .sample(
                shots,
                separate_observables=True,
            )
        )