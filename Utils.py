from qiskit.quantum_info.operators import Operator
import numpy as np
import math
import cmath
MESSAGE_INPUT_ERROR = "Invalid input given."
MESSAGE_TOO_MANY_QUBITS_ERROR = "Too many qubits used. Please use 5 qubits or less."
MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR = "Too many qubits used for tensor setting. Please use 3 qubits or less."
MESSAGE_INVALID_GATE_ERROR = "Invalid gate(s) used."
MESSAGE_UNKNOWN_ERROR = "UNKNOWN ERROR"
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
                [0.+0.j, 0.+0.j, 0+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
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
CX_BE_ONE_GAP = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j]])

CX_LE_ONE_GAP = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
                [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]])

CY_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 0-1.j],
                [0.+0.j, 0.+0.j, 0+1.j, 0+0.j]])


CY_BE_ONE_GAP = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.-1.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j, 0.+0.j]])

CY_LE_ONE_GAP = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.-1.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j, 1.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.-1.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j, 0.+0.j]])


def get_cp(phi, num_gap_qubits=0) :
    if num_gap_qubits == 1:
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * phi), 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0., 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * phi)]])
    else: 
        return []
    
def get_crx(theta, little_endian=False, num_gap_qubits=0):
    if little_endian:
        if num_gap_qubits == 1:
            return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2)-1.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, math.sin(theta/2)-1.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2)-1.j, math.cos(theta/2)+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2)-1.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j]])
    else:
        if num_gap_qubits == 1:
            return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, math.sin(theta/2)-1.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2)-1.j, math.cos(theta/2)+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, math.sin(theta/2)-1.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2)-1.j, math.cos(theta/2)+0.j]])
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, math.sin(theta/2)-1.j],
                [0.+0.j, 0.+0.j, 1+0.j, 0+0.j],
                [0.+0.j, math.sin(theta/2)-1.j, 0+1.j, math.cos(theta/2)+0.j]])

def get_cry(theta, num_gap_qubits = 0):
    if num_gap_qubits == 1:
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, -math.sin(theta/2), 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, -math.sin(theta/2)],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2), 0.+0.j, math.cos(theta/2)+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, math.sin(theta/2), 0.+0.j, math.cos(theta/2)+0.j]])
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, math.cos(theta/2)+0.j, 0.+0.j, -math.sin(theta/2)+0.j],
                [0.+0.j, 0.+0.j, 1+0.j, 0+0.j],
                [0.+0.j, math.sin(theta/2)+0.j, 0+1.j, math.cos(theta/2)+0.j]])

def get_crz(theta, num_gap_qubits = 0):
    if num_gap_qubits == 1:
         return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, -cmath.exp(-1j * theta / 2), 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, -cmath.exp(-1j * theta / 2), 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(-1j * theta / 2), 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(-1j * theta / 2)]])       
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0+0.j],
                [0.+0.j, 0.+0.j, cmath.exp(-1j * theta / 2), 0+0.j],
                [0.+0.j, 0+0.j, 0+0.j, cmath.exp(-1j * theta / 2)]])

def get_non_neighbouring_LE_matrix(gate):
    name = gate.operation.name
    match name:
        case "cp":
            return get_cp(gate.operation.params[0], 1)
        case "crx":
            return get_crx(gate.operation.params[0], True, 1)
        case "cx":
            return CX_LE_ONE_GAP
        case "cy":
            return CY_LE_ONE_GAP
        case _:
            return []