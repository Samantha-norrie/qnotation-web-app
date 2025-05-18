from qiskit.circuit.library import *
from qiskit.quantum_info.operators import Operator
import numpy as np
from enum import Enum
import math
import cmath
import copy
from errors import GateNotImplementedError
from GateInformation import GateInformation

CIRCUIT_GATE_LOOP = '''    gate_list = []\n
    for gate in qc.data:\n\
        qubit_indices = [qc.find_bit(q).index for q in gate.qubits]
        gate_list.append({"name": gate.name, "qubit_indices": qubit_indices, "params": gate.params})\n
    print([qc.num_qubits, gate_list])\n'''

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
MESSAGE_GATE_NOT_SUPPORTED_ERROR = "Gate(s) not supported."
MESSAGE_HIGHER_INDEXED_CONTROL_QUBIT_ERROR = "One or more control qubits have an index higher than their respective target qubit(s)"
MESSAGE_NON_NEIGHBOURING_QUBITS_ERROR = "Multi-qubit gate(s) contain non-neighbouring qubits"
MESSAGE_UNKNOWN_ERROR = "UNKNOWN ERROR"
class GateNames(Enum):
    CONTROLLED_CONTROLLED_X = "ccx"
    CONTROLLED_CONTROLLED_Z = "ccz"
    CONTROLLED_HADAMARD = "ch"
    CONTROLLED_PHASE = "cp"
    CONTROLLED_ROTAIONAL_X = "crx"
    CONTROLLED_ROTAIONAL_Y = "cry"
    CONTROLLED_ROTAIONAL_Z = "crz"
    CONTROLLED_S_DAGGER = "csdg"
    CONTROLLED_S = "cs"
    CONTROLLED_SWAP = "cswap"
    CONTROLLED_SQUARED_X = "csx"
    CONTROLLED_U = "cu"
    CONTROLLED_X = "cx"
    CONTROLLED_Y = "cy"
    CONTROLLED_Z = "cz"
    DOUBLE_CONTROLLED_X = "dcx"
    DIAGONAL = "d"
    GLOBAL_PHASE = "gp"
    HADAMARD = "h"
    IDENTITY = "i"
    MULTI_CONTROLLED_MULTI_TARGET = "mcmt"
    MULTI_CONTROLLED_PHASE = "mcp"
    MULTI_CONTROLLED_X = "mcx"
    PERMUTATION = "permutation"
    PHASE = "p"
    QUANTUM_FOURIER_TRANSFORM = "qft"
    RELATIVE_PHASE_CONTROLLED_X = "rc3x"
    RELATIVE_PHASE_CONTROLLED_CONTROLLED_X = "rccx"
    ROTATIONAL = "r"
    ROTATIONAL_V = "rv"
    ROTATIONAL_X = "rx"
    ROTATIONAL_X_X = "rxx"
    ROTATIONAL_Y = "ry"
    ROTATIONAL_Y_Y = "ryy"
    ROTATIONAL_Z = "rz"
    ROTATIONAL_Z_X = "rzx"
    ROTATIONAL_Z_Z = "rzz"
    S_DAGGER = "sdg"
    S = "s"
    SWAP = "swap"
    SQUARED_X_DAGGER = "sxdg"
    SQUARED_X = "sx"
    T_ADJOINT = "tdg"
    T = "t"
    U = "u"
    UNIFORMLY_CONTROLLED = "uc"
    UNITARY = "unitary"
    X = "x"
    X_X_MINUS_Y_Y = "xxminusyy"
    X_X_PLUS_Y_Y = "xxplusyy"
    Y = "y"
    Z = "z"

CONTROL_TARGET_GATE_NAMES = [ "ch", "cp", "crx", "cry", "crz","cs","csdg", "csx","cswap","cx", "cy", "cz", 
                            "csx", "cu", "mcp", "mcx"]
CONTROL_CONTROL_TARGET_GATE_NAMES = ["ccx", "ccz","rccx"]
CONTROL_CONTROL_CONTROL_TARGET_GATE_NAMES = ["rcccx"]

IDENTITY_MATRIX = np.array([[1, 0], [0, 1]])

MAX_NUM_QUBITS_FOR_APP = 5
MAX_NUM_QUBITS_FOR_TENSOR = 3

def get_gate_object_from_gate_name(gate_name, params=[]):
    match gate_name:
        case GateNames.CONTROLLED_CONTROLLED_X.value:
            return CCXGate()
        case GateNames.CONTROLLED_CONTROLLED_Z.value:
            return CCZGate()
        case GateNames.CONTROLLED_PHASE.value:
            return CPhaseGate(params[0])
        case GateNames.CONTROLLED_ROTAIONAL_X.value:
            return CRXGate(params[0])
        case GateNames.CONTROLLED_ROTAIONAL_Y.value:
            return CRYGate(params[0])
        case GateNames.CONTROLLED_ROTAIONAL_Z.value:
            return CRZGate(params[0])
        case GateNames.CONTROLLED_S_DAGGER.value:
            return CSdgGate()
        case GateNames.CONTROLLED_S.value:
            return CSGate()
        case GateNames.CONTROLLED_SQUARED_X:
            return CSXGate()
        case GateNames.CONTROLLED_U.value:
            return CUGate(params[0], params[1], params[2], params[3])
        case GateNames.CONTROLLED_X.value:
            return CXGate()
        case GateNames.CONTROLLED_Y.value:
            return CYGate()
        case GateNames.CONTROLLED_Z.value:
            return CZGate()
        case GateNames.DOUBLE_CONTROLLED_X.value:
            return DCXGate()
        case GateNames.DIAGONAL.value:
            return DiagonalGate(params[0])
        case GateNames.GLOBAL_PHASE.value:
            return GlobalPhaseGate(params[0])
        case GateNames.HADAMARD.value:
            return HGate()
        case GateNames.IDENTITY.value:
            return IGate()
        case GateNames.MULTI_CONTROLLED_MULTI_TARGET.value:
            return MCMTGate()
        case GateNames.MULTI_CONTROLLED_PHASE.value:
            return MCPhaseGate()
        case GateNames.MULTI_CONTROLLED_X.value:
            return MCXGate()
        case GateNames.PERMUTATION.value:
            return PermutationGate(params[0])
        case GateNames.PHASE.value:
            return PhaseGate(params[0])
        case GateNames.QUANTUM_FOURIER_TRANSFORM.value:
            return QFTGate()
        case GateNames.RELATIVE_PHASE_CONTROLLED_CONTROLLED_X.value:
            return RCCXGate()
        case GateNames.RELATIVE_PHASE_CONTROLLED_X.value:
            return RC3XGate()
        case GateNames.ROTATIONAL.value:
            return RGate(params[0], params[1])
        case GateNames.ROTATIONAL_V.value:
            return RVGate(params[0], params[1], params[2])
        case GateNames.ROTATIONAL_X.value:
            return RXGate(params[0])
        case GateNames.ROTATIONAL_X_X.value:
            return RXXGate(params[0])
        case GateNames.ROTATIONAL_Y.value:
            return RYGate(params[0])
        case GateNames.ROTATIONAL_Y_Y.value:
            return RYYGate(params[0])
        case GateNames.ROTATIONAL_Z.value:
            return RZGate(params[0])
        case GateNames.ROTATIONAL_Z_X.value:
            return RZXGate(params[0])
        case GateNames.ROTATIONAL_Z_Z.value:
            return RZZGate(params[0])
        case GateNames.S.value:
            return SGate()
        case GateNames.S_DAGGER.value:
            return SdgGate()
        case GateNames.SWAP.value:
            return SwapGate()
        case GateNames.T.value:
            return TGate()
        case GateNames.T_ADJOINT.value:
            return TdgGate()
        case GateNames.U.value:
            return UGate(params[0], params[1], params[2])
        case GateNames.UNIFORMLY_CONTROLLED.value:
            return UCGate(params[0])
        case GateNames.X.value:
            return XGate()
        case GateNames.X_X_MINUS_Y_Y.value:
            return XXMinusYYGate(params[0], params[1])
        case GateNames.X_X_PLUS_Y_Y.value:
            return XXPlusYYGate(params[0], params[1])
        case GateNames.Y.value:
            return YGate()
        case GateNames.Z.value:
            return ZGate()
        case _:
            raise GateNotImplementedError

# MULTI-QUBIT HANDLING
SQRT2_INV= 1 / np.sqrt(2)

CCX_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]])

CCZ_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                   [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, -1.+0.j]])

CH_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, SQRT2_INV, SQRT2_INV],
                [0.+0.j, 0.+0.j, SQRT2_INV, -SQRT2_INV]])

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

CY_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, 0+0.j, 0-1.j],
                [0.+0.j, 0.+0.j, 0+1.j, 0+0.j]])

RCCX_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, -1.+0.j, 0.+0.j]])

RCX_BE = np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                        [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
                        [0.+0.j, 0.+0.j, -1.+0.j, 0.+0.j]])
def get_cp_be(phi):
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * phi)]])
    
def get_crx_be(theta, little_endian=False, num_gap_qubits=0):
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

def get_cu_be(theta, phi, lam, gamma): 
    return  np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j,  0.+0.j],
                [0.+0.j, 0.+0.j, cmath.exp(1j * gamma) * math.cos(theta / 2), -cmath.exp(1j * (lam+ gamma)) * math.sin(theta / 2)],
                [0.+0.j,  0.+0.j, cmath.exp(1j * (phi+ gamma)) * math.sin(theta / 2), cmath.exp(1j * (phi + lam+ gamma)) * math.cos(theta / 2)]])

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

def get_mcp_be(lam, num_qubits):
    if num_qubits == 2:
        return get_cp_be(lam)
    elif num_qubits == 3:
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0., 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * lam)]])
    elif num_qubits == 4:
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0., 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * lam)]])
    elif num_qubits == 5:
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0., 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * lam)]])
    else:
        raise GateNotImplementedError()
    
def get_ryy_be(theta):
    return np.array([[math.cos(theta/2)+0.j, 0.+0.j, 0.+0.j, -1j*math.sin(theta/2)+0.j],
                        [0.+0.j, math.cos(theta/2)+0.j, 1j*math.sin(theta/2)+0.j, 0.+0.j],
                        [0.+0.j, 1j*math.sin(theta/2)+0.j, math.cos(theta/2)+0.j, 0.+0.j],
                        [-1j*math.sin(theta/2)+0.j, 0.+0.j, 0.+0.j, math.cos(theta/2)+0.j]])
def get_rzx_be(theta):
    return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, math.cos(theta/2)+0.j, 1j*math.sin(theta/2)+0.j],
                            [0.+0.j, 0.+0.j, 1j*math.sin(theta/2)+0.j, math.cos(theta/2)+0.j]])
        
def get_matrix_for_multi_qubit_big_endian(gate: GateInformation):
    name = gate.get_name()
    match name:
        case GateNames.CONTROLLED_CONTROLLED_X.value:
            return CCX_BE        
        case GateNames.CONTROLLED_CONTROLLED_Z.value:
            return CCZ_BE
        case GateNames.CONTROLLED_HADAMARD.value:
            return CH_BE
        case GateNames.CONTROLLED_PHASE.value:
            phi = gate.get_params()[0]
            return get_cp_be(phi)
        case GateNames.CONTROLLED_ROTAIONAL_X.value:
            theta = gate.get_params()[0]
            return get_crx_be(theta)
        case GateNames.CONTROLLED_ROTAIONAL_Y.value:
            theta = gate.get_params()[0]
            return get_cry(theta)
        case GateNames.CONTROLLED_ROTAIONAL_Z.value:
            theta = gate.get_params()[0]
            return get_crz(theta)
        case GateNames.CONTROLLED_S_DAGGER.value:
            return gate.get_matrix()
        case GateNames.CONTROLLED_S.value:
            return gate.get_matrix()
        case GateNames.CONTROLLED_SQUARED_X.value:
            return CSX_BE
        case GateNames.CONTROLLED_SWAP.value:
            return CSWAP_BE
        case GateNames.CONTROLLED_U.value:
            params = gate.get_params()
            theta = params[0]
            phi = params[1]
            lam = params[2]
            gamma = params[3]
            return get_cu_be(theta, phi, lam, gamma)
        case GateNames.CONTROLLED_X.value:
            return CX_BE
        case GateNames.CONTROLLED_Y.value:
            return CY_BE
        case GateNames.CONTROLLED_Z.value:
            return gate.get_matrix()
        case GateNames.DOUBLE_CONTROLLED_X.value:
            return gate.get_matrix()
        case GateNames.MULTI_CONTROLLED_PHASE.value:
            lam = gate.get_params[0]
            return get_mcp_be(lam, gate.get_num_qubits())
        case GateNames.RELATIVE_PHASE_CONTROLLED_CONTROLLED_X.value:
            return RCCX_BE
        case GateNames.RELATIVE_PHASE_CONTROLLED_X.value:
            return RCX_BE
        case GateNames.ROTATIONAL_X_X.value:
            return gate.get_matrix()
        case GateNames.ROTATIONAL_Y_Y.value:
            return get_ryy_be(theta)
        case GateNames.ROTATIONAL_Z_X.value:
            theta = gate.get_params()[0]
            return get_rzx_be(theta)
        case GateNames.ROTATIONAL_Z_Z.value:
            return gate.get_matrix()
        case _:
            return []
