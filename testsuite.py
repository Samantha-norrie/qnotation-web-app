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

    def test_circuit_dirac_little_endian(self):
        pass

    def test_circuit_dirac_big_endian(self):
        pass

    def test_matrix_equation_little_endian(self):
        pass

    def test_matrix_equation_big_endian(self):
        pass

    def test_matrix_state_little_endian(self):
        pass

    def test_matrix_state_big_endian(self):
        pass


class TestSingleColumnTwoQubitNeighbouringGateReverse(TestQNotation):
    @classmethod
    def setup_class(cls):
        cls.data = asyncio.run(
            send_request(SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE_REVERSE)
        )

    def test_status_code(self):
        assert self.data["status"] == SUCCESS

    def test_circuit_dirac_little_endian(self):
        pass

    def test_circuit_dirac_big_endian(self):
        pass

    def test_matrix_equation_little_endian(self):
        pass

    def test_matrix_equation_big_endian(self):
        pass

    def test_matrix_state_little_endian(self):
        pass

    def test_matrix_state_big_endian(self):
        pass
