from qiskit.quantum_info.operators import Operator
import numpy as np
import math
import cmath

CONTROL = "CONTROL"
TARGET = "TARGET"
AUXILIARY = "AUXILIARY"
NOT_INVOLVED = "NOT INVOLVED"

GATE_INFO = "GATE INFO"

STATE = "STATE"
GATE = "GATE"

IDENTITY_MATRIX_NAME = "I"

MESSAGE_INPUT_ERROR = "Invalid input given."
MESSAGE_TOO_MANY_QUBITS_ERROR = "Too many qubits used. Please use 5 qubits or less."
MESSAGE_TOO_MANY_QUBITS_FOR_TENSOR_ERROR = "Too many qubits used for tensor setting. Please use 3 qubits or less."
MESSAGE_INVALID_GATE_ERROR = "Invalid gate(s) used."
MESSAGE_UNKNOWN_ERROR = "UNKNOWN ERROR"

CONTROL_TARGET_GATE_NAMES = [ "ch", "cp", "crx", "cry", "crz","cs","csdg", "csx","cswap","cx", "cy", "cz", 
                            "csx", "cu", "mcp", "mcx"]
CONTROL_CONTROL_TARGET_GATE_NAMES = ["ccx", "ccz","rccx"]
CONTROL_CONTROL_CONTROL_TARGET_GATE_NAMES = ["rcccx"]

IDENTITY_MATRIX = np.array([[1, 0], [0, 1]])

MAX_NUM_QUBITS_FOR_APP = 5
MAX_NUM_QUBITS_FOR_TENSOR = 3

def get_list_of_qubit_indices_in_gate(gate):
    """
    Gives list of qubits involved in given gate

    Args:
        gate (CircuitInstruction): the gate to be checked

    Returns:
        list[int]: list of qubit indices
    """
    index_list = []
    for i in range(0, len(gate.qubits)):
        index_list.append(gate.qubits[i].index)

    return index_list

def is_non_neighbouring_gate(gate):
    """
    Checks if given gate has non-neighbouring qubits

    Args:
        gate (CircuitInstruction): the gate to be checked

    Returns:
        boolean: True if the given gate contains non-neighbouring qubits
    """
    num_qubits = len(gate.qubits)
    if num_qubits > 1:

        indices = get_list_of_qubit_indices_in_gate(gate).sort()

        for i in range(1, len(indices)):
            if indices[i] - indices[i-1] > 1:
                return True
               
    return False

# MULTI-QUBIT HANDLING

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

def get_non_neighbouring_matrix_little_endian(gate):
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
        
def get_matrix_for_multi_qubit_big_endian(gate):
    name = gate.operation.name
    non_neighbouring = is_non_neighbouring_gate(gate)
    match name:
        case "ch":
            return CH_BE
        case "cp":
            if non_neighbouring:
                phi = gate.operation.params[0]
                if non_neighbouring:
                    return get_cp(phi, 1)
                return get_cp()
            return Operator(gate.operation).data 
        case "crx":
            theta = gate.operation.params[0]
            if non_neighbouring:
                return get_crx(theta, False, 1)
            return get_crx(theta)
        case "cry":
            theta = gate.operation.params[0]
            if non_neighbouring:
                return get_cry(theta,1)
            return get_cry(theta)
        case "crz":
            theta = gate.operation.params[0]
            if non_neighbouring:
                return get_crz(theta, 1)
            return get_crz(theta)
        case "cs":
            return Operator(gate.operation).data
        case "csx":
            return CSX_BE
        case "cswap":
            return CSWAP_BE
        case "cx":
            if non_neighbouring:
                return CX_BE_ONE_GAP
            return CX_BE
        case "cy":
            if non_neighbouring:
                return CY_BE_ONE_GAP
            return CY_BE
        case "cz":
            return Operator(gate.operation).data 
        case _:
            return []