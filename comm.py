from flask import Flask, jsonify, request
from Notation import Notation
from qiskit import *
from qiskit.circuit import CircuitInstruction, Instruction, Qubit
from qiskit.circuit.quantumcircuitdata import QuantumCircuitData

app = Flask(__name__)

@app.post("/get_notation_data")
def get_notation_data():
    data = request.form.to_dict()


    display_tensor_product =  bool(data.get('data[display_tensor_product]'))
    qc_string = data.get('data[qc]')
    circuit_details = Notation.process_circuit_received(qc_string)

    qc = QuantumCircuit(circuit_details[0])
    gate_list = QuantumCircuitData(qc)
    print("INIT type", type(gate_list))
    # gate_list.__setitem__(0, circuit_details[1][0])
    # for i in range(0, len(circuit_details[1])):
    #     qc.h(0)

    for i in range(0, len(circuit_details[1])):
        qc.data.insert(i, circuit_details[1][i])
    # gate_list.append(circuit_details[1][0])

    # qc.data = gate_list#QuantumCircuitData(circuit_details[1])
    # print(" type AFTER", type(gate_list))
    print("DATA", qc.data)
    print(qc)


    # qc.x(0)
    # qc.x(1)
    # qc.h(0)
    # qc.h(1)

    # qc.h(2)
    # print("DATA", type(qc.data[0]))

    # print("PROPOSED", type(circuit_details[1]))
    # print("COMPARISON", (qc.data[0] == circuit_details[1][0]))
    # qc.data = circuit_details[1]
    # for i in range(0, len(circuit_details[1])):
    #     qc.data.append(circuit_details[1][i])



    num_qubits = qc.num_qubits

    grouped_gates = Notation.group_gates(qc)

    matrix_gates = Notation.create_matrix_gate_json(num_qubits, grouped_gates)
    matrix_state_vectors = Notation.create_matrix_state_vector_json(num_qubits, matrix_gates)

    dirac_state_vectors = Notation.format_matrix_state_vectors_for_dirac_state(matrix_state_vectors)

    print("dirac states", dirac_state_vectors)

    # if display_tensor_product:
    #     matrix_gates

    matrix_gates.insert(0, matrix_state_vectors[0])

    circuit_dirac_gates= Notation.create_circuit_dirac_gates_json(num_qubits, grouped_gates)

    return jsonify({'matrix_gates': matrix_gates,
                    'matrix_state_vectors': matrix_state_vectors,
                    'circuit_dirac_gates': circuit_dirac_gates,
                    'dirac_state_vectors': dirac_state_vectors,
        'success': 'ok'})

if __name__ == "__main__":
    app.run(port=8001, debug=True)