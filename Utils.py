from qiskit.quantum_info.operators import Operator
import numpy as np
import math
import cmath
MESSAGE_TOO_MANY_QUBITS_FOR_APP = "Too many qubits used. Please use 5 qubits or less."
MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR = "Too many qubits used for tensor setting. Please use 3 qubits or less."
MESSAGE_INVALID_GATE = "Invalid gate(s) used."
MESSAGE_UNKNOWN_ERROR = "Unknown error."
NEUTRAL_GATE_TYPE = "NEUTRAL"
BETWEEN_GATE_TYPE = "BETWEEN"
CONTROL_GATE_TYPE = "CONTROL"
TARGET_GATE_TYPE = "TARGET"
CONTROL_TARGET_GATE_NAMES = [ "ch", "cp", "crx", "cry", "crz","cs","csdg", "csx","cswap","cx", "cy", "cz", 
                            "csx", "cu", "mcp", "mcx"]
CONTROL_CONTROL_TARGET_GATE_NAMES = ["ccx", "ccz","rccx"]
CONTROL_CONTROL_CONTROL_TARGET_GATE_NAMES = ["rcccx"]

CH_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.70710678+0.j, 0.70710678+0.j],
                [0.+0.j, 0.+0.j, 0.70710678+0.j, -0.70710678+0.j]])

CSWAP_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 1+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]
                [0.+0.j, 0.+0.j, 0+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j]])



CSX_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.5+0.5j, 0.5-0.5j],
                [0.+0.j, 0.+0.j, 0.5-0.5j, 0.5+0.5j]])

CX_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 1+0.j],
                [0.+0.j, 0.+0.j, 1+0.j, 0+0.j]])

CY_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 0-1.j],
                [0.+0.j, 0.+0.j, 0+1.j, 0+0.j]])

# No need to cover cz because the matrices are the same

def get_crx(theta):
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, math.sin(theta/2)-1.j],
                [0.+0.j, 0.+0.j, 1+0.j, 0+0.j],
                [0.+0.j, math.sin(theta/2)-1.j, 0+1.j, math.cos(theta/2)+0.j]])

def get_cry(theta):
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, -math.sin(theta/2)+0.j],
                [0.+0.j, 0.+0.j, 1+0.j, 0+0.j],
                [0.+0.j, math.sin(theta/2)+0.j, 0+1.j, math.cos(theta/2)+0.j]])

def get_crz(theta):
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0+0.j],
                [0.+0.j, 0.+0.j, cmath.exp(-1j * theta / 2), 0+0.j],
                [0.+0.j, 0+0.j, 0+0.j, cmath.exp(-1j * theta / 2)]])