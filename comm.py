from flask import Flask, jsonify, request, send_from_directory
from Notation import Notation
from flask_cors import CORS
from qiskit import *
from Utils import MESSAGE_TOO_MANY_QUBITS_ERROR, MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR, MESSAGE_INVALID_GATE_ERROR, MESSAGE_INPUT_ERROR, MESSAGE_UNKNOWN_ERROR
from Errors import TooManyQubitsError, TooManyQubitsForTensorError, InvalidGateError, InputError

import os


app = Flask(__name__, static_folder='../qnotation_node/build')

CORS(app, resources={r"/*":{"origins": "https://qnotation.vercel.app/"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.post("/get_notation_data")
def get_notation_data():
    data = request.form.to_dict()

    qc_string = data.get('data[qc]')
    matrix_gates_le = None
    matrix_gates_be = None
    matrix_gates_tensor_product_le = None
    matrix_gates_tensor_product_be = None
    matrix_state_vector_le = None
    matrix_state_vector_be = None
    circuit_dirac_gate_le = None
    circuit_dirac_gate_be = None
    dirac_state_vector_le = None
    dirac_state_vector_be = None
    num_qubits = 0
    message = ""
    status = 200

    little_endian = True
    
    try:
        circuit_details = Notation.process_circuit_received(qc_string)

        qc = Notation.convert_input_gates(circuit_details[0], circuit_details[1]) #.reverse_bits()

        num_qubits = qc.num_qubits
        if num_qubits > 5 : 
            raise TooManyQubitsError

        grouped_gates_le = Notation.group_gates(num_qubits, qc.copy(), little_endian)
        grouped_gates_be = Notation.group_gates(num_qubits, qc)
        # print("grouped gates le", grouped_gates_le)
        # print("grouped gates be", grouped_gates_be)

        matrix_gates_le = Notation.create_matrix_gate_json(num_qubits, grouped_gates_le, little_endian)
        matrix_gates_be = Notation.create_matrix_gate_json(num_qubits, grouped_gates_be)

        matrix_state_vector_le = Notation.create_matrix_state_vector_json(num_qubits, matrix_gates_le)
        matrix_state_vector_be = Notation.create_matrix_state_vector_json(num_qubits, matrix_gates_be)

        matrix_gates_le = Notation.simplify_values_matrix(matrix_gates_le)
        matrix_gates_be = Notation.simplify_values_matrix(matrix_gates_be)

        dirac_state_vector_le = Notation.format_matrix_state_vectors_for_dirac_state(num_qubits, matrix_state_vector_le)
        dirac_state_vector_be = Notation.format_matrix_state_vectors_for_dirac_state(num_qubits, matrix_state_vector_be)
        if num_qubits <= 3:
            matrix_gates_tensor_product_le = Notation.create_tensor_product_matrix_gate_json(num_qubits, grouped_gates_le, True)
            matrix_gates_tensor_product_le.insert(0, matrix_state_vector_le[0])

            matrix_gates_tensor_product_be = Notation.create_tensor_product_matrix_gate_json(num_qubits, grouped_gates_be)
            matrix_gates_tensor_product_be.insert(0, matrix_state_vector_be[0])

        matrix_gates_le.insert(0, matrix_state_vector_le[0])
        matrix_gates_be.insert(0, matrix_state_vector_be[0])

        circuit_dirac_gate_le= Notation.create_circuit_dirac_gates_json(num_qubits, grouped_gates_le)
        circuit_dirac_gate_be= Notation.create_circuit_dirac_gates_json(num_qubits, grouped_gates_be)
    except TooManyQubitsError:
        message = MESSAGE_TOO_MANY_QUBITS_ERROR
        status = 500
    except TooManyQubitsForTensorError:
        message = MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR
        status = 500
    except InvalidGateError:
        message = MESSAGE_INVALID_GATE_ERROR
        status = 500
    except InputError:
        message = MESSAGE_INPUT_ERROR
        status = 500
    # except Exception as e:
    #     print("ERROR ", e)
    #     message = MESSAGE_UNKNOWN_ERROR
    #     status = 520


    return jsonify({'matrix_gates_le': matrix_gates_le,
                    'matrix_gates_be': matrix_gates_be,
                    'matrix_gates_tensor_product_le': matrix_gates_tensor_product_le,
                    'matrix_gates_tensor_product_be': matrix_gates_tensor_product_be,
                    'matrix_state_vector_le': matrix_state_vector_le,
                    'matrix_state_vector_be': matrix_state_vector_be,
                    'circuit_dirac_gate_le': circuit_dirac_gate_le,
                    'circuit_dirac_gate_be': circuit_dirac_gate_be,
                    'dirac_state_vector_le': dirac_state_vector_le,
                    'dirac_state_vector_be': dirac_state_vector_be,
                    'num_qubits': num_qubits,
                    'message': message,
        'status': status})


if __name__ == "__main__":
    app.run(port=8001, debug=True)