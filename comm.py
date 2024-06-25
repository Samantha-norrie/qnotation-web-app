from flask import Flask, jsonify, request
from Notation import Notation
from qiskit import *

app = Flask(__name__)

@app.post("/get_notation_data")
def get_notation_data():
    data = request.form.to_dict()


    display_tensor_product =  bool(data.get('data[display_tensor_product]'))
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    qc.x(0)
    qc.h(1)
    # qc.h(2)

    num_qubits = qc.num_qubits

    grouped_gates = Notation.group_gates(qc)

    matrix_gates = Notation.create_matrix_gate_json(num_qubits, grouped_gates)
    matrix_state_vectors = Notation.create_matrix_state_vector_json(num_qubits, matrix_gates)

    if display_tensor_product:
        matrix_gates

    matrix_gates.insert(0, matrix_state_vectors[0])

    circuit_dirac_gates= Notation.create_circuit_dirac_gates_json(num_qubits, grouped_gates)

    return jsonify({'matrix_gates': matrix_gates,
                    'matrix_state_vectors': matrix_state_vectors,
                    'circuit_dirac_gates': circuit_dirac_gates,
                    'dirac_state': "",
        'success': 'ok'})

if __name__ == "__main__":
    app.run(port=8001, debug=True)