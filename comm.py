from flask import Flask, jsonify, request
from Notation import Notation
from qiskit import *
from Utils import MESSAGE_TOO_MANY_QUBITS_FOR_APP, MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR, MESSAGE_INVALID_GATE, MESSAGE_UNKNOWN_ERROR
from Errors import TooManyQubitsForApp, TooManyQubitsForTensor, InvalidGate

app = Flask(__name__)

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
            raise TooManyQubitsForApp

        grouped_gates_le = Notation.group_gates(num_qubits, qc.copy(), little_endian)
        grouped_gates_be = Notation.group_gates(num_qubits, qc)

        # if not little_endian:


        print("GROUPED GATES LE", grouped_gates_le)
        print("GROUPED GATES BE", grouped_gates_be)
        # no extra gates added at this point

        matrix_gates_le = Notation.create_matrix_gate_json(num_qubits, grouped_gates_le, little_endian)
        matrix_gates_be = Notation.create_matrix_gate_json(num_qubits, grouped_gates_be)
        print("AFTER MATRIX", matrix_gates_le)
        print("AFTER MATRIX", matrix_gates_be)

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
    except TooManyQubitsForApp:
        message = MESSAGE_TOO_MANY_QUBITS_FOR_APP
        status = 500
    except TooManyQubitsForTensor:
        message = MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR
        status = 500
    except InvalidGate:
        message = MESSAGE_INVALID_GATE
        status = 500
    except Exception as e:
        print("ERROR ", e)
        message = MESSAGE_UNKNOWN_ERROR
        status = 520

    # print("TENSOR", matrix_gates_tensor_product)
    # print("CONDENSED", matrix_gates)
    print("matrix_gates_le", matrix_gates_le)
    print("matrix_gates_be", matrix_gates_be)
    print("matrix_gates_tensor_product_le", matrix_gates_tensor_product_le)
    print("matrix_gates_tensor_product_be", matrix_gates_tensor_product_be)
    print('matrix_state_vector_le', matrix_state_vector_le)
    print('matrix_state_vector_be', matrix_state_vector_be)
    print('circuit_dirac_gate_le', circuit_dirac_gate_le)
    print('circuit_dirac_gate_be', circuit_dirac_gate_be)
    print('dirac_state_vector_le', dirac_state_vector_le)
    print('dirac_state_vector_be', dirac_state_vector_be)
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
    # return jsonify({'matrix_gates_le': matrix_gates_le,
    #             'matrix_gates_be': matrix_gates_le,
    #             'matrix_gates_tensor_product_le': matrix_gates_tensor_product_le,
    #             'matrix_gates_tensor_product_be': matrix_gates_tensor_product_le,
    #             'matrix_state_vector_le': matrix_state_vector_le,
    #             'matrix_state_vector_be': matrix_state_vector_le,
    #             'circuit_dirac_gate_le': circuit_dirac_gate_le,
    #             'circuit_dirac_gate_be': circuit_dirac_gate_le,
    #             'dirac_state_vector_le': dirac_state_vector_le,
    #             'dirac_state_vector_be': dirac_state_vector_le,
    #             'num_qubits': num_qubits,
    #             'message': message,
    # 'status': status})

if __name__ == "__main__":
    app.run(port=8001, debug=True)