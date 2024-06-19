from qiskit import QuantumCircuit
from Notation import Notation

# class Tests:
def test_hadamard_column():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    result = Notation.group_gates(circuit)
    print("Result\n"+ str(result))
    assert len(result)==1

def test_hadamard_two_column():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    result = Notation.group_gates(circuit)
    print("Result\n"+ str(result))
    assert len(result)==2

def test_cnot_three_qubits():
    circuit = QuantumCircuit(3)
    circuit.cx(1,2)
    result = Notation.group_gates(circuit)
    print("Result\n"+ str(result))
    assert len(result)==1

def test_hadamard_cnot_two_column():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(1,2)
    circuit.h(0)
    circuit.cx(1,2)
    result = Notation.group_gates(circuit)
    print("Result\n"+ str(result))
    assert len(result)==2 

def test_hadamard_three_column():
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
    result = Notation.group_gates(circuit)
    print("Result\n"+ str(result))
    assert len(result)==3

    # def circuit_formatting_hadamard_column():

    #     circuit = QuantumCircuit(3)
    #     circuit.h(0)
    #     circuit.h(1)
    #     circuit.h(2)

    #     result = Notation.create_circuit_json(3, Notation.group_gates(circuit))
    #     print("Result\n"+ str(result))

    # def matrix_gate_formatting_hadamard_column():

    #     circuit = QuantumCircuit(3)
    #     circuit.h(0)
    #     circuit.h(1)
    #     circuit.h(2)

    #     result = Notation.create_matrix_gate_json(3, Notation.group_gates(circuit))
    #     print("Result\n"+ str(result))
    #     print("Result\n"+ str(Notation.create_matrix_state_vector_json(3, result)))


# Tests.hadamard_column_test()
# Tests.hadamard_two_column_test()
# Tests.cnot_three_qubits_test()
# Tests.hadamard_cnot_two_column_test()
#
# Tests.hadamard_three_column_test()
# Tests.circuit_formatting_hadamard_column()
# Tests.matrix_gate_formatting_hadamard_column()

# Notation.create_matrix_state_vector_json(2)
