import pennylane as qml
import numpy as np
from parsers.pennylane_parser import PennylaneParser

# dev = qml.device("default.qubit", wires=2)

# @qml.qnode(dev)
# def qc():
#     qml.Hadamard(wires=0)
#     qml.CNOT(wires=[0, 1])
#     return qml.state()

# qc()

# print(qc._tape.operations[0].wires.tolist())
# print(dev.wires.tolist())
BELL_STATE_PENNYLANE = "import pennylane as qml\nimport numpy as np\ndev = qml.device(\"default.qubit\", wires=2)\n@qml.qnode(dev)\ndef qc():\n\tqml.Hadamard(wires=0)\n\tqml.CNOT(wires=[0, 1])\n\treturn qml.state()\nqc()"
# print(PennylaneParser.convert_code_string_to_circuit_object(BELL_STATE_PENNYLANE))
pp = PennylaneParser()
pp.run_pipeline(BELL_STATE_PENNYLANE)


