import subprocess
import tempfile
import sys
import os
from enum import Enum
import pennylane as qml

from errors import InputError

def run_code_string_in_temp_file(code_string):
    """
    Takes code as a string, runs it inside a temp file, and returns what is received from stdout

    Args:
       code_string (String): string of code to be run

    Returns:
        Unknown: what is received from stdout
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code_string.encode("utf-8"))
        temp_file_name = temp_file.name
    try:
        result = subprocess.run(
            [sys.executable, temp_file_name], capture_output=True, text=True, timeout=5
        )
        print("ERR", result.stderr)
        print("stdout", result.stdout)
        output = eval(result.stdout, {"qml": qml})


    except Exception as e:
        print("input error caught in process_circuit_received:", e)
        raise InputError
    finally:

        # Ensure the temporary file is deleted after execution
        os.remove(temp_file_name)

    return output

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

def get_multi_qubit_gate_le()
    pass

QISKIT_CIRCUIT_GATE_LOOP = '''    gate_list = []\n
    for gate in qc.data:\n\
        qubit_indices = [qc.find_bit(q).index for q in gate.qubits]
        gate_list.append({"name": gate.name, "qubit_indices": qubit_indices, "params": gate.params})\n
    print([qc.num_qubits, gate_list])\n'''

PENNYLANE_CIRCUIT_GATE_LOOP = '''\ngate_list = []\n
for op in qc._tape.operations:\n
    gate_list.append({"name": op.name, "wires": op.wires.tolist(), "params": op.parameters, "matrix": op.matrix()})\n
print([dev.wires.tolist(), gate_list])\n'''

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

CONTROL_TARGET_GATE_NAMES = [ "ch", "cp", "crx", "cry", "crz","cs","csdg", "csx","cswap","cx", "cy", "cz", "cu", "mcp", "mcx"]
CONTROL_CONTROL_TARGET_GATE_NAMES = ["ccx", "ccz","rccx"]
CONTROL_CONTROL_CONTROL_TARGET_GATE_NAMES = ["rcccx"]
