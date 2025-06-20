import cirq
import numpy as np
def main():
    qubit0 = cirq.LineQubit(0)
    qubit1 = cirq.LineQubit(1)
    circuit = cirq.Circuit()
    circuit.append([cirq.H(qubit0),cirq.CNOT(qubit0, qubit1)])

    gate_list = []

    for gate in circuit.all_operations():

        gate_list.append({"name": str(gate.gate), "qubit_indices": gate.qubits, "params": cirq.parameter_names(gate.gate), "matrix": cirq.unitary(gate.gate)})
    print(len(circuit.all_qubits()), gate_list)
main()