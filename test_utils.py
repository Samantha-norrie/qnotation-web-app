import httpx
import asyncio
import json

EMPTY = ""
NO_GATES = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\n"
TYPO = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\nqv.h(0)"
TOO_MANY_QUBITS = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(100)\n\n# Insert code below\nqc.h(0)"
SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE = "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\nqc.cx(0, 1)\n"
SINGLE_COLUMN_TWO_QUBIT_NEIGHBOURING_GATE_REVERSE= "from qiskit import *\nimport numpy as np\nqc = QuantumCircuit(2)\n\n# Insert code below\nqc.cx(1, 0)\n"

URL = "http://127.0.0.1:8001/get_notation_data"
HEADERS= {"Content-Type": "application/json"}
SUCCESS = 200
SERVER_ERR = 500
BAD_REQUEST_ERR = 400
async def send_request(qc_string):

    payload = {"qc": qc_string}
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=payload, headers=HEADERS)
        return response.json()