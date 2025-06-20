import cirq
import numpy as np
from parsers.cirq_parser import CirqParser

# qubit0 = cirq.LineQubit(0)
# qubit1 = cirq.LineQubit(1)
# circuit = cirq.Circuit()

# circuit.append([cirq.H(qubit0),cirq.H(qubit1),cirq.CNOT(qubit0, qubit1)])
# # print("circuit", circuit.all_operations())
# for gate in circuit.all_operations():
#     print(gate.gate)
BELL_STATE_PENNYLANE = "import cirq\nimport numpy as np\nqubit0 = cirq.LineQubit(0)\nqubit1 = cirq.LineQubit(1)\ncircuit = cirq.Circuit()\ncircuit.append([cirq.H(qubit0),cirq.CNOT(qubit0, qubit1)])"
# print(PennylaneParser.convert_code_string_to_circuit_object(BELL_STATE_PENNYLANE))
cp = CirqParser()
cp.run_pipeline(BELL_STATE_PENNYLANE)

