import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from quantum_library_parsers import ParserFactory
from errors import QNotationException, MESSAGE_UNKNOWN_ERROR

app = Flask(__name__)

#CORS(app, resources={r"/*": {"origins": "https://qnotation.vercel.app"}})
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

@app.post("/notation_data")
def notation_data():

    data = request.get_json()

    qc_string = data.get("qc_string")
    qc_type = data.get("qc_type")

    matrix_gate_little_endian = None
    matrix_gate_big_endian = None
    matrix_gate_tensor_little_endian = None
    matrix_gate_tensor_big_endian = None
    matrix_state_little_endian = None
    matrix_state_big_endian = None
    circuit_dirac_gate_little_endian = None
    circuit_dirac_gate_big_endian = None
    dirac_state_little_endian = None
    dirac_state_big_endian = None
    num_qubits = 0
    message = ""
    status = 200

    try:
        parser = ParserFactory.get_parser(qc_type)
        return jsonify(parser.run_pipeline(qc_string))
    except QNotationException as e:
        print(f"QNOTATION ERROR {e}")
        message = ""
        status = 400
    except Exception as e:
        print(f"ERROR {e}")
        message = MESSAGE_UNKNOWN_ERROR
        status = 500

    json_to_return = jsonify(
        {
            "matrix_gate_little_endian": matrix_gate_little_endian,
            "matrix_gate_big_endian": matrix_gate_big_endian,
            "matrix_gate_tensor_little_endian": matrix_gate_tensor_little_endian,
            "matrix_gate_tensor_big_endian": matrix_gate_tensor_big_endian,
            "matrix_state_little_endian": matrix_state_little_endian,
            "matrix_state_big_endian": matrix_state_big_endian,
            "circuit_dirac_gate_little_endian": circuit_dirac_gate_little_endian,
            "circuit_dirac_gate_big_endian": circuit_dirac_gate_big_endian,
            "dirac_state_little_endian": dirac_state_little_endian,
            "dirac_state_big_endian": dirac_state_big_endian,
            "num_qubits": num_qubits,
            "message": message,
            "status": status,
        }
    )

    return json_to_return

if __name__ == "__main__":
    app.run(port=8000, debug=True)
