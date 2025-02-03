from qiskit import QuantumCircuit
from Notation import NotationQiskit
from test_utils import TEST_CIRCUIT_FORMATTING_HADAMARD_COLUMN_OUTPUT, TEST_MATRIX_GATE_FORMATTING_HADAMARD_COLUMN_OUTPUT_MATRIX, TEST_MATRIX_GATE_FORMATTING_HADAMARD_COLUMN_OUTPUT_VECTOR

# SIZE BASED TESTS 

def test_hadamard_column_length():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    result = NotationQiskit.group_gates(circuit)
    assert len(result) == 1 and len(result[0]) == 3

def test_hadamard_two_column_length():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    result = NotationQiskit.group_gates(circuit)
    assert len(result) == 2 and len(result[1]) == 3

def test_cnot_three_qubits_length():
    circuit = QuantumCircuit(3)
    circuit.cx(1,2)
    result = NotationQiskit.group_gates(circuit)
    assert len(result) == 1 and len(result[0]) == 1

def test_hadamard_cnot_two_column_length():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(1,2)
    circuit.h(0)
    circuit.cx(1,2)
    result = NotationQiskit.group_gates(circuit)
    assert len(result) == 2 and len(result[0]) == 2

def test_hadamard_three_column_length():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    result = NotationQiskit.group_gates(circuit)
    assert len(result) == 3 and len(result[2]) == 3

# OUTPUT TESTS
def test_circuit_formatting_hadamard_column_output():

    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    result = NotationQiskit.create_circuit_dirac_gates_json(3, NotationQiskit.group_gates(circuit))
    assert result == TEST_CIRCUIT_FORMATTING_HADAMARD_COLUMN_OUTPUT

def test_matrix_gate_formatting_hadamard_column_output():

    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    result = NotationQiskit.create_matrix_gate_json(3, NotationQiskit.group_gates(circuit))
    assert result == TEST_MATRIX_GATE_FORMATTING_HADAMARD_COLUMN_OUTPUT_MATRIX

    result = NotationQiskit.create_matrix_state_vector_json(3, result)
    assert result == TEST_MATRIX_GATE_FORMATTING_HADAMARD_COLUMN_OUTPUT_VECTOR
