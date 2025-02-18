import httpx
import asyncio
import json
import pytest
from abc import ABC, abstractmethod

EMPTY = ""
NO_GATES = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\n"
TYPO = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\nqv.h(0)"
SINGLE_QUBIT_SINGLE_HADAMARD = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(1)\n\n# Insert code below\nqc.h(0)"
TOO_MANY_QUBITS = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(100)\n\n# Insert code below\nqc.h(0)"
SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\nqc.cx(0, 1)\n"
SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE_REVERSE = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\nqc.cx(1, 0)\n"

URL = "http://127.0.0.1:8001/get_notation_data"
HEADERS = {"Content-Type": "application/json"}
SUCCESS = 200
SERVER_ERR = 500
BAD_REQUEST_ERR = 400

MATRIX_GATE_LITTLE_ENDIAN = "matrix_gate_little_endian"
MATRIX_GATE_BIG_ENDIAN = "matrix_gate_big_endian"
MATRIX_GATE_TENSOR_LITTLE_ENDIAN = "matrix_gate_tensor_little_endian"
MATRIX_GATE_TENSOR_BIG_ENDIAN = "matrix_gate_tensor_big_endian"
MATRIX_STATE_VECTOR_LITTLE_ENDIAN = "matrix_state_vector_little_endian"
MATRIX_STATE_VECTOR_BIG_ENDIAN = "matrix_state_vector_big_endian"
CIRCUIT_DIRAC_GATE_LITTLE_ENDIAN = "circuit_dirac_gate_little_endian"
CIRCUIT_DIRAC_GATE_BIG_ENDIAN = "circuit_dirac_gate_big_endian"
DIRAC_STATE_VECTOR_LITTLE_ENDIAN = "dirac_state_vector_little_endian"
DIRAC_STATE_VECTOR_BIG_ENDIAN = "dirac_state_vector_big_endian"
STATUS = "status"

# SINGLE-QUBIT HADAMARD
RESULTS_SINGLE_QUBIT_SINGLE_HADAMARD = {
    "circuit_dirac_gate_big_endian": [
        {"content": [[0]], "key": 0, "type": "STATE"},
        {
            "content": [{"gate": "H", "gate_type": "GATE INFO"}],
            "key": 1,
            "type": "GATE",
        },
    ],
    "circuit_dirac_gate_little_endian": [
        {"content": [[0]], "key": 0, "type": "STATE"},
        {
            "content": [{"gate": "H", "gate_type": "GATE INFO"}],
            "key": 1,
            "type": "GATE",
        },
    ],
    "dirac_state_vector_big_endian": [
        {"content": [{"bin": "0", "scalar": 1}], "key": 0, "type": "STATE"},
        {
            "content": [{"bin": "0", "scalar": 0.71}, {"bin": "1", "scalar": 0.71}],
            "key": 1,
            "type": "STATE",
        },
    ],
    "dirac_state_vector_little_endian": [
        {"content": [{"bin": "0", "scalar": 1}], "key": 0, "type": "STATE"},
        {
            "content": [{"bin": "0", "scalar": 0.71}, {"bin": "1", "scalar": 0.71}],
            "key": 1,
            "type": "STATE",
        },
    ],
    "matrix_gate_big_endian": [
        {"content": [[1], [0]], "key": 0, "type": "STATE"},
        {"content": [[0.71, 0.71], [0.71, -0.71]], "key": 1, "type": "GATE"},
    ],
    "matrix_gate_little_endian": [
        {"content": [[1], [0]], "key": 0, "type": "STATE"},
        {"content": [[0.71, 0.71], [0.71, -0.71]], "key": 1, "type": "GATE"},
    ],
    "matrix_gate_tensor_big_endian": [
        {"content": [[1], [0]], "key": 0, "type": "STATE"},
        {"content": [[[0.71, 0.71], [0.71, -0.71]]], "key": 1, "type": "GATE"},
    ],
    "matrix_gate_tensor_little_endian": [
        {"content": [[1], [0]], "key": 0, "type": "STATE"},
        {"content": [[[0.71, 0.71], [0.71, -0.71]]], "key": 1, "type": "GATE"},
    ],
    "matrix_state_vector_big_endian": [
        {"content": [[1], [0]], "key": 0, "type": "STATE"},
        {"content": [[0.71], [0.71]], "key": 1, "type": "GATE"},
    ],
    "matrix_state_vector_little_endian": [
        {"content": [[1], [0]], "key": 0, "type": "STATE"},
        {"content": [[0.71], [0.71]], "key": 1, "type": "GATE"},
    ],
    "message": "",
    "num_qubits": 1,
    "status": 200,
}


async def send_request(qc_string):

    payload = {"qc": qc_string}
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=payload, headers=HEADERS)
        return response.json()


class TestQNotation(ABC):
    """Abstract base class for test cases"""

    @abstractmethod
    def test_status_code(self):
        pass

    @abstractmethod
    def test_circuit_dirac_little_endian(self):
        pass

    @abstractmethod
    def test_circuit_dirac_big_endian(self):
        pass

    @abstractmethod
    def test_dirac_state_little_endian(self):
        pass

    @abstractmethod
    def test_dirac_state_big_endian(self):
        pass

    @abstractmethod
    def test_matrix_gate_little_endian(self):
        pass

    @abstractmethod
    def test_matrix_gate_big_endian(self):
        pass

    @abstractmethod
    def test_matrix_gate_tensor_little_endian(self):
        pass

    @abstractmethod
    def test_matrix_gate_tensor_big_endian(self):
        pass

    @abstractmethod
    def test_matrix_state_little_endian(self):
        pass

    @abstractmethod
    def test_matrix_state_big_endian(self):
        pass
