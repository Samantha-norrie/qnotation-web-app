MESSAGE_TOO_MANY_QUBITS_FOR_APP = "Too many qubits used. Please use 5 qubits or less."
MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR = "Too many qubits used for tensor setting. Please use 3 qubits or less."
MESSAGE_INVALID_GATE = "Invalid gate(s) used."
MESSAGE_UNKNOWN_ERROR = "Unknown error."
NEUTRAL_GATE_TYPE = "NEUTRAL"
BETWEEN_GATE_TYPE = "BETWEEN"
CONTROL_GATE_TYPE = "CONTROL"
TARGET_GATE_TYPE = "TARGET"
CONTROL_TARGET_GATE_NAMES = [ "ch", "cp", "crx", "cry", "crz","cs","csdg","cswap","cx", "cy", "cz", 
                            "csx", "cu", "mcp", "mcx"]
CONTROL_CONTROL_TARGET_GATE_NAMES = ["ccx", "ccz","rccx"]
CONTROL_CONTROL_CONTROL_TARGET_GATE_NAMES = ["rcccx"]