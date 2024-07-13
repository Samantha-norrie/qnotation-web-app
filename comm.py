from flask import Flask, jsonify, request
from Notation import Notation
from qiskit import *
from Utils import MESSAGE_TOO_MANY_QUBITS_FOR_APP, MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR, MESSAGE_INVALID_GATE, MESSAGE_UNKNOWN_ERROR
from Errors import TooManyQubitsForApp, TooManyQubitsForTensor, InvalidGate

app = Flask(__name__)

@app.post("/get_notation_data")
def get_notation_data():
    data = request.form.to_dict()


    display_tensor_product =  bool(data.get('data[display_tensor_product]'))
    qc_string = data.get('data[qc]')
    matrix_gates = None
    matrix_state_vectors = None
    circuit_dirac_gates = None
    dirac_state_vectors = None
    message = ""
    status = 200
    
    try:
        circuit_details = Notation.process_circuit_received(qc_string)

        qc = Notation.convert_input_gates(circuit_details[0], circuit_details[1])

        num_qubits = qc.num_qubits
        if num_qubits > 5 : 
            raise TooManyQubitsForApp
        elif num_qubits > 3 and display_tensor_product:
            raise TooManyQubitsForTensor

        grouped_gates = Notation.group_gates(qc)

        matrix_gates = Notation.create_matrix_gate_json(num_qubits, grouped_gates)
        print("MATRICES", matrix_gates)
        matrix_state_vectors = Notation.create_matrix_state_vector_json(num_qubits, matrix_gates)

        matrix_gates = Notation.simplify_values_matrix(matrix_gates)

        dirac_state_vectors = Notation.format_matrix_state_vectors_for_dirac_state(matrix_state_vectors)

        matrix_gates.insert(0, matrix_state_vectors[0])

        circuit_dirac_gates= Notation.create_circuit_dirac_gates_json(num_qubits, grouped_gates)
    except TooManyQubitsForApp:
        message = MESSAGE_TOO_MANY_QUBITS_FOR_APP
        status = 500
    except TooManyQubitsForTensor:
        message = MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR
        status = 500
    except InvalidGate:
        message = MESSAGE_INVALID_GATE
        status = 500
    except:
        message = MESSAGE_UNKNOWN_ERROR
        status = 500

    return jsonify({'matrix_gates': matrix_gates,
                    'matrix_state_vectors': matrix_state_vectors,
                    'circuit_dirac_gates': circuit_dirac_gates,
                    'dirac_state_vectors': dirac_state_vectors,
                    'message': message,
        'status': status})

if __name__ == "__main__":
    app.run(port=8001, debug=True)