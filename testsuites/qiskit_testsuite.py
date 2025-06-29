import asyncio
from .test_utils import *

class TestEmpty(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(EMPTY, super().qc_type))

    def test_status_code(self):
        assert self.data[STATUS] == BAD_REQUEST_ERR

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 0

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] is None

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] is None

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] is None

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] is None

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] is None

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] is None

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] is None

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] is None

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] is None

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] is None


class TestTypo(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(QISKIT_TYPO, super().qc_type))

    def test_status_code(self):
        assert self.data[STATUS] == BAD_REQUEST_ERR

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 0

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] is None

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] is None

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] is None

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] is None

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] is None

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] is None

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] is None

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] is None

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] is None

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] is None


class TestSingleQubitSingleHadamard(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(QISKIT_SINGLE_QUBIT_SINGLE_HADAMARD, super().qc_type))

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 1

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[DIRAC_STATE_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[DIRAC_STATE_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_STATE_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_STATE_BIG_ENDIAN]


class TestSingleColumnTwoQubitNeighbouringGate(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(QISKIT_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE, super().qc_type))

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 2

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[DIRAC_STATE_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[DIRAC_STATE_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_STATE_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] == QISKIT_RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_STATE_BIG_ENDIAN]

class TestBellStateThreeQubits(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(QISKIT_BELL_STATE_THREE_QUBITS, super().qc_type)
        )

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 3

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[DIRAC_STATE_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[DIRAC_STATE_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_STATE_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_STATE_BIG_ENDIAN]

class TestHigherIndexedControlQubit(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(QISKIT_HIGHER_CONTROL_QUBIT_INDEX, super().qc_type)
        )

    def test_status_code(self):
        assert self.data["status"] == BAD_REQUEST_ERR

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[NUM_QUBITS]

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[DIRAC_STATE_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[DIRAC_STATE_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_STATE_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_STATE_BIG_ENDIAN]

class TestNonNeighbouringQubits(TestQiskit):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(QISKIT_NON_NEIGHBOURING_QUBITS, super().qc_type)
        )

    def test_status_code(self):
        assert self.data["status"] == BAD_REQUEST_ERR

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == RESULTS_NON_NEIGHBOURING_QUBITS[NUM_QUBITS]

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[DIRAC_STATE_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[DIRAC_STATE_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_STATE_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_STATE_BIG_ENDIAN]

