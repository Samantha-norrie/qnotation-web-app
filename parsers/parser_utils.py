import subprocess
import tempfile
import sys
import os
import copy
from enum import Enum
import pennylane as qml
from qiskit.circuit.library import *
import numpy as np

from errors import InputError, GateNotImplementedError

def insert_main_function_into_code_string(start_main_after: str, code_string: str, output_string: str) -> str:
    """
    Adds a main function and its call to the given code string.

    Args:
        start_main_after (str): the line to insert the main header after
        code_string (str): the code where the main function should be inserted into
        output_string (str): the code responsible for printing out circuit information
    """
    code_lines = code_string.split("\n")
    code_string_formatted = ""
    end_of_imports_found = False

    for i in range(0, len(code_lines)):
        if not end_of_imports_found and start_main_after in code_lines[i]:
            code_string_formatted = (
                code_string_formatted + code_lines[i] + "\ndef main():\n"
            )
            end_of_imports_found = True
        elif end_of_imports_found:
            code_string_formatted = code_string_formatted + "    "+ code_lines[i] + "\n"
        else:
            code_string_formatted = code_string_formatted + code_lines[i] + "\n"\

    code_string_formatted = (
        code_string_formatted +  output_string + "\nmain()\n"
    )

    return code_string_formatted

def simplify_single_matrix(matrix):
    """
    Simplifies matrix TODO: improve simplification logic

    Args:
        matrix (list[complex]): a list of matrices representing the columns in the quantum circuit

    Returns:
        list[object]: Simplified matrix
    """

    for j in range(0, len(matrix)):
        for k in range(0, len(matrix[j])):

            real_val = float(matrix[j][k].real)
            imag_val = float(matrix[j][k].imag)

            if real_val == 0.0 and imag_val == 0.0:
                matrix[j][k] = 0.00
            elif round(imag_val, 4) == 0.0:
                matrix[j][k] = float("{:.2f}".format(real_val))
            elif round(imag_val, 4) == 1.0:
                matrix[j][k] = " i "
            else:
                matrix[j][k] = "{:.2f}".format(real_val + imag_val) + "i"
    return matrix

def get_control_and_target_qubit_indices(gate_name, indices):
    """
    Gets control and target qubits of a quantum gate

    Args:
        gate (CircuitInstruction): the gate to be checked

    Returns:
        list[int], list[int]: a sorted list of control qubit indices, a sorted list of target qubit indices
    """
    control_qubit_indices = []
    target_qubit_indices = []
    print(gate_name, indices)

    if len(indices) == 1:
        control_qubit_indices.append(indices[0])

    elif gate_name in CONTROL_TARGET_GATE_NAMES:
        control_qubit_indices.append(indices[0])
        target_qubit_indices.append(indices[1])

    elif gate_name in CONTROL_CONTROL_TARGET_GATE_NAMES:
        control_qubit_indices.append(indices[0])
        control_qubit_indices.append(indices[1])
        target_qubit_indices.append(indices[2])

    else:
        control_qubit_indices.append(indices[0])
        control_qubit_indices.append(indices[1])
        control_qubit_indices.append(indices[2])
        target_qubit_indices.append(indices[3])

    control_qubit_indices.sort()
    target_qubit_indices.sort()

    return control_qubit_indices, target_qubit_indices

def simplify_values_state_vector(state_vector):

    for i in range(0, len(state_vector)):
        real_val = float(state_vector[i][0].real)
        imag_val = float(state_vector[i][0].imag)

        if real_val == 0.0 and imag_val == 0.0:
            state_vector[i][0] = 0.0
        elif round(imag_val, 4) == 0.0:

            state_vector[i][0] = float(round(real_val, 2))
        elif round(imag_val, 4) == 1.0:
            state_vector[i][0] = "i"
        else:
            state_vector[i][0] = str(round(real_val, 2)) + str(round(imag_val, 2)) + "i"

    return state_vector

def get_qiskit_gate_object_from_gate_name(gate_name, params=[]):
    match gate_name:
        case GateNames.CONTROLLED_CONTROLLED_X.value:
            return CCXGate()
        case GateNames.CONTROLLED_CONTROLLED_Z.value:
            return CCZGate()
        case GateNames.CONTROLLED_HADAMARD.value:
            return CHGate()
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
        case GateNames.CONTROLLED_SQUARED_X.value:
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
def get_multi_qubit_gate_le():
    pass

QISKIT_CIRCUIT_GATE_LOOP = '''    gate_list = []\n
    for gate in qc.data:\n
        qubit_indices = [qc.find_bit(q).index for q in gate.qubits]\n
        gate_list.append({"name": gate.name, "qubit_indices": qubit_indices, "params": gate.params})\n
    print([qc.num_qubits, gate_list])\n'''

PENNYLANE_CIRCUIT_GATE_LOOP = '''\ngate_list = []\n
for op in qc._tape.operations:\n
    gate_list.append({"name": op.name, "wires": op.wires.tolist(), "params": op.parameters, "matrix": op.matrix()})\n
print([len(dev.wires.tolist()), gate_list])\n'''

CIRQ_CIRCUIT_GATE_LOOP = '''\n    gate_list = []\n
    for gate in circuit.all_operations():\n
        gate_list.append({"name": str(gate.gate), "qubit_indices": gate.qubits, "params": cirq.parameter_names(gate.gate), "matrix": cirq.unitary(gate.gate)})\n
    print(len(circuit.all_qubits()), gate_list)'''

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
    IDENTITY = "id"
    MULTI_CONTROLLED_MULTI_TARGET = "mcmt"
    MULTI_CONTROLLED_PHASE = "mcp"
    MULTI_CONTROLLED_X = "mcx"
    PERMUTATION = "permutation"
    PHASE = "p"
    QUANTUM_FOURIER_TRANSFORM = "qft"
    RELATIVE_PHASE_CONTROLLED_X = "rcccx"
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

IDENTITY_MATRIX = np.array([[1, 0], [0, 1]])

CONTROL_TARGET_GATE_NAMES = [ "ch", "cp", "crx", "cry", "crz","cs","csdg", "csx","cswap","cx", "cnot","cy", "cz", "cu", "mcp", "mcx"]
CONTROL_CONTROL_TARGET_GATE_NAMES = ["ccx", "ccz","rccx"]
CONTROL_CONTROL_CONTROL_TARGET_GATE_NAMES = ["rcccx"]


CONTROL = "CONTROL"
TARGET = "TARGET"
AUXILIARY = "AUXILIARY"
NOT_INVOLVED = "NOT INVOLVED"

GATE_INFO = "GATE INFO"

STATE = "STATE"
GATE = "GATE"

IDENTITY_MATRIX_NAME = "I"

MAX_NUM_QUBITS_FOR_APP = 5
MAX_NUM_QUBITS_FOR_TENSOR = 3

NUMPY_IMPORT_STRING = "import numpy as np"
