from qiskit.circuit.library import *
from qiskit.quantum_info.operators import Operator
import numpy as np
from enum import Enum
import math
import cmath
import copy
from errors import GateNotImplementedError
from GateInformation import GateInformation

# CIRCUIT_GATE_LOOP = '''\tgate_list = []\n
# \tfor gate in qc.data:\n\
# \tqubit_indices = [qc.find_bit(q).index for q in gate.qubits]
# \tgate_list.append({"name": gate.name, "qubit_indices": qubit_indices, "params": gate.params})\n
# \tprint([qc.num_qubits, gate_list])\n'''

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
MESSAGE_UNKNOWN_ERROR = "UNKNOWN ERROR"
class GateNames(Enum):
    CONTROLLED_THREE_QUBIT_SQUARED_X = "c3sx"
    CONTROLLED_THREE_QUBIT_X = "c3x"
    CONTROLLED_FOUR_QUBIT_X = "c4x"
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
    UNIFORMLY_CONTROLLED_PAULI_ROTATIONAL = "ucpr"
    UNIFORMLY_CONTROLLED_ROTATIONAL_X = "ucrx"
    UNIFORMLY_CONTROLLED_ROTATIONAL_Y = "ucry"
    UNIFORMLY_CONTROLLED_ROTATIONAL_Z = "ucrz"
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
        case GateNames.CONTROLLED_THREE_QUBIT_SQUARED_X.value:
            return C3SXGate()
        case GateNames.CONTROLLED_THREE_QUBIT_X.value:
            return C3XGate()
        case GateNames.CONTROLLED_FOUR_QUBIT_X.value:
            return C4XGate()
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
        case GateNames.UNIFORMLY_CONTROLLED_PAULI_ROTATIONAL.value:
            return UCPauliRotGate(params[0], params[1])
        case GateNames.UNIFORMLY_CONTROLLED_ROTATIONAL_X.value:
            return UCRXGate(params[0])
        case GateNames.UNIFORMLY_CONTROLLED_ROTATIONAL_Y.value:
            return UCRYGate(params[0])
        case GateNames.UNIFORMLY_CONTROLLED_ROTATIONAL_Z.value:
            return UCRZGate(params[0])
        case GateNames.UNIFORMLY_CONTROLLED_ROTATIONAL_Z.value:
            return UnitaryGate()
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

def is_non_neighbouring_gate(gate):
    """
    Checks if given gate has non-neighbouring qubits

    Args:
        gate (GateInformation): the gate to be checked

    Returns:
        boolean: True if the given gate contains non-neighbouring qubits
    """
    
    
    if gate.get_num_qubits() > 1:

        sorted_indices = copy.deepcopy(gate.get_control_qubit_indices() + gate.get_target_qubit_indices())
        sorted_indices.sort()

        for i in range(1, len(sorted_indices)):
            if sorted_indices[i] - sorted_indices[i-1] > 1:
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

# TODO update for bigger gaps
def get_non_neighbouring_matrix_little_endian(gate: GateInformation):
    name = gate.get_name()
    match name:
        case "cp":
            return get_cp(gate.get_params(), 1)
        case "crx":
            return get_crx(gate.get_params(), True, 1)
        case "cx":
            return CX_LE_ONE_GAP
        case "cy":
            return CY_LE_ONE_GAP
        case _:
            raise GateNotImplementedError()
        
def get_matrix_for_multi_qubit_big_endian(gate: GateInformation):
    name = gate.get_name()
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
