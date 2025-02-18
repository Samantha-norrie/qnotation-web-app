from flask import Flask, jsonify, request, send_from_directory
from notation import *
from flask_cors import CORS
from qiskit import *
from preprocessing_utils import (
    process_circuit_received,
    group_gates,
    create_gate_information_list_for_gates,
)
from utils import (
    MESSAGE_TOO_MANY_QUBITS_ERROR,
    MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR,
    MESSAGE_INVALID_GATE_ERROR,
    MESSAGE_INPUT_ERROR,
    MESSAGE_UNKNOWN_ERROR,
)
from errors import (
    TooManyQubitsError,
    TooManyQubitsForTensorError,
    InvalidGateError,
    InputError,
)

import os


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://qnotation.vercel.app"}})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.post("/get_notation_data")
def get_notation_data():

    data = request.json
    qc_string = data.get("qc")

    matrix_gate_little_endian = None
    matrix_gate_big_endian = None
    matrix_gate_tensor_little_endian = None
    matrix_gate_tensor_big_endian = None
    matrix_state_vector_little_endian = None
    matrix_state_vector_big_endian = None
    circuit_dirac_gate_little_endian = None
    circuit_dirac_gate_big_endian = None
    dirac_state_vector_little_endian = None
    dirac_state_vector_big_endian = None
    num_qubits = 0
    message = ""
    status = 200

    try:

        # 1.0. Transform Qiskit code received into a QuantumCircuit
        qc = process_circuit_received(qc_string)
        num_qubits = qc.num_qubits

        # 2.0. Transform quantum circuit into GateInformation objects
        gates_and_indices = create_gate_information_list_for_gates(qc)

        # 3.0. Group gates into operations. These operations will be referred to as 'columns' to match frontend visualizations
        grouped_gates_big_endian, grouped_gates_little_endian = group_gates(
            num_qubits, gates_and_indices.copy()
        )

        # 4.0. Create data for equation and state parts of matrix component

        # 4.1. Compute matrices for each column
        matrix_gate_big_endian = create_matrix_gate_json(
            num_qubits, grouped_gates_big_endian
        )
        matrix_gate_little_endian = create_matrix_gate_json(
            num_qubits, grouped_gates_little_endian, True
        )

        # 4.2. Compute state vectors
        matrix_state_vector_little_endian = create_matrix_state_vector_json(
            num_qubits, matrix_gate_little_endian
        )
        matrix_state_vector_big_endian = create_matrix_state_vector_json(
            num_qubits, matrix_gate_big_endian
        )

        # 4.3. Create tensor product lists for each column if appropriate
        if num_qubits <= MAX_NUM_QUBITS_FOR_TENSOR:
            matrix_gate_tensor_little_endian = create_tensor_product_matrix_gate_json(
                num_qubits, grouped_gates_little_endian, True
            )
            matrix_gate_tensor_little_endian.insert(
                0, matrix_state_vector_little_endian[0]
            )

            matrix_gate_tensor_big_endian = create_tensor_product_matrix_gate_json(
                num_qubits, grouped_gates_big_endian
            )
            matrix_gate_tensor_big_endian.insert(0, matrix_state_vector_big_endian[0])

        # 4.4. Simplify matrices for frontend display
        matrix_gate_little_endian = simplify_matrices_json(matrix_gate_little_endian)
        matrix_gate_big_endian = simplify_matrices_json(matrix_gate_big_endian)

        matrix_gate_little_endian.insert(0, matrix_state_vector_little_endian[0])
        matrix_gate_big_endian.insert(0, matrix_state_vector_big_endian[0])

        # 5.0. Create data for equation and state parts of circuit and Dirac components
        circuit_dirac_gate_little_endian = create_circuit_dirac_gates_json(
            num_qubits, grouped_gates_little_endian
        )
        circuit_dirac_gate_big_endian = create_circuit_dirac_gates_json(
            num_qubits, grouped_gates_big_endian
        )

        dirac_state_vector_little_endian = (
            format_matrix_state_vectors_for_dirac_state_json(
                num_qubits, matrix_state_vector_little_endian
            )
        )
        dirac_state_vector_big_endian = (
            format_matrix_state_vectors_for_dirac_state_json(
                num_qubits, matrix_state_vector_big_endian
            )
        )

    except TooManyQubitsError:
        message = MESSAGE_TOO_MANY_QUBITS_ERROR
        status = 400
    except TooManyQubitsForTensorError:
        message = MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR
        status = 400
    except InvalidGateError:
        message = MESSAGE_INVALID_GATE_ERROR
        status = 400
    except GateNotImplementedError:
        message = MESSAGE_GATE_NOT_SUPPORTED_ERROR
        status = 400
    except InputError:
        message = MESSAGE_INPUT_ERROR
        status = 400
    except Exception as e:
        print("ERROR ", e)
        message = MESSAGE_UNKNOWN_ERROR
        status = 500

    return jsonify(
        {
            "matrix_gate_little_endian": matrix_gate_little_endian,
            "matrix_gate_big_endian": matrix_gate_big_endian,
            "matrix_gate_tensor_little_endian": matrix_gate_tensor_little_endian,
            "matrix_gate_tensor_big_endian": matrix_gate_tensor_big_endian,
            "matrix_state_vector_little_endian": matrix_state_vector_little_endian,
            "matrix_state_vector_big_endian": matrix_state_vector_big_endian,
            "circuit_dirac_gate_little_endian": circuit_dirac_gate_little_endian,
            "circuit_dirac_gate_big_endian": circuit_dirac_gate_big_endian,
            "dirac_state_vector_little_endian": dirac_state_vector_little_endian,
            "dirac_state_vector_big_endian": dirac_state_vector_big_endian,
            "num_qubits": num_qubits,
            "message": message,
            "status": status,
        }
    )


if __name__ == "__main__":
    app.run(port=8001, debug=True)
