import pytest
import httpx
import asyncio
import json
from test_utils import *


class TestEmpty(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(EMPTY))

    def test_status_code(self):
        assert self.data[STATUS] == BAD_REQUEST_ERR

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 0

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == None

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == None

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == None

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == None

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == None

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == None

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == None

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == None

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == None

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == None


class TestTypo(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(TYPO))

    def test_status_code(self):
        assert self.data[STATUS] == BAD_REQUEST_ERR

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 0

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == None

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == None

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == None

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == None

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == None

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == None

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == None

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == None

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == None

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == None


class TestSingleQubitSingleHadamard(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(SINGLE_QUBIT_SINGLE_HADAMARD))

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 1

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[DIRAC_STATE_VECTOR_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[DIRAC_STATE_VECTOR_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_STATE_VECTOR_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD[MATRIX_STATE_VECTOR_BIG_ENDIAN]


class TestSingleColumnTwoQubitNeighbouringGate(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(send_request(SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE))

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

    def test_num_qubits(self):
        assert self.data[NUM_QUBITS] == 2

    def test_circuit_dirac_little_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN]

    def test_circuit_dirac_big_endian(self):
        assert self.data[CIRCUIT_DIRAC_GATE_BIG_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[CIRCUIT_DIRAC_GATE_BIG_ENDIAN]

    def test_dirac_state_little_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[DIRAC_STATE_VECTOR_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[DIRAC_STATE_VECTOR_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_STATE_VECTOR_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == RESULTS_SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE[MATRIX_STATE_VECTOR_BIG_ENDIAN]

class TestBellStateThreeQubits(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(BELL_STATE_THREE_QUBITS)
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
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[DIRAC_STATE_VECTOR_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[DIRAC_STATE_VECTOR_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_STATE_VECTOR_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == RESULTS_BELL_STATES_THREE_QUBITS[MATRIX_STATE_VECTOR_BIG_ENDIAN]

class TestHigherIndexedControlQubit(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(HIGHER_CONTROL_QUBIT_INDEX)
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
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[DIRAC_STATE_VECTOR_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[DIRAC_STATE_VECTOR_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_STATE_VECTOR_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == RESULTS_HIGHER_CONTROL_QUBIT_INDEX[MATRIX_STATE_VECTOR_BIG_ENDIAN]

class TestNonNeighbouringQubits(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(NON_NEIGHBOURING_QUBITS)
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
        assert self.data[DIRAC_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[DIRAC_STATE_VECTOR_LITTLE_ENDIAN]

    def test_dirac_state_big_endian(self):
        assert self.data[DIRAC_STATE_VECTOR_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[DIRAC_STATE_VECTOR_BIG_ENDIAN]

    def test_matrix_gate_little_endian(self):
        assert self.data[MATRIX_GATE_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_LITTLE_ENDIAN]

    def test_matrix_gate_big_endian(self):
        assert self.data[MATRIX_GATE_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_BIG_ENDIAN]

    def test_matrix_gate_tensor_little_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_TENSOR_LITTLE_ENDIAN]

    def test_matrix_gate_tensor_big_endian(self):
        assert self.data[MATRIX_GATE_TENSOR_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_GATE_TENSOR_BIG_ENDIAN]

    def test_matrix_state_little_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_LITTLE_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_STATE_VECTOR_LITTLE_ENDIAN]

    def test_matrix_state_big_endian(self):
        assert self.data[MATRIX_STATE_VECTOR_BIG_ENDIAN] == RESULTS_NON_NEIGHBOURING_QUBITS[MATRIX_STATE_VECTOR_BIG_ENDIAN]

