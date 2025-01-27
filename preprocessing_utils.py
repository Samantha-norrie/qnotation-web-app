from qiskit import *
from qiskit.quantum_info.operators import Operator
from qiskit.circuit import CircuitInstruction, Instruction, Qubit
from errors import InvalidGateError, InputError
import subprocess
import sys
import os
import tempfile
from utils import * 
from notation import notation

# TODO Remove once gate id issue stemming from temp file is resolved
def apply_gate_to_circuit(qc, gate):
    """
    Applies gate to QuantumCircuit

    Args:
        qc (QuantumCircuit): QuantumCircuit that gate should be applied to
        gate (CircuitInstruction): Gate that will be applied to qc

    """

    match gate.operation.name:
        case "cp":
            qc.cp(gate.operation.params[0], gate.qubits[0].index, gate.qubits[1].index)       
        case "cs":
            qc.cs(gate.qubits[0].index, gate.qubits[1].index)
        case "cswap":
            qc.cswap(gate.qubits[0].index, gate.qubits[1].index, gate.qubits[2].index)
        case "crx":
            qc.crx(gate.operation.params[0], gate.qubits[0].index, gate.qubits[1].index)
        case "csx":
            qc.csx(gate.qubits[0].index, gate.qubits[1].index)
        case "cx":
            qc.cx(gate.qubits[0].index, gate.qubits[1].index)
        case "cy":
            qc.cy(gate.qubits[0].index, gate.qubits[1].index)
        case "cz":
            qc.cz(gate.qubits[0].index, gate.qubits[1].index)
        case "dcx":
            qc.dcx(gate.qubits[0].index, gate.qubits[1].index)
        case "h":
            qc.h(gate.qubits[0].index)
        case "iswap":
            qc.iswap(gate.qubits[0].index, gate.qubits[1].index)
        case "p":
            qc.p(gate.operation.params[0], gate.qubits[0].index)
        case "r":
            qc.r(gate.operation.params[0], gate.operation.params[1], gate.qubits[0].index)
        case "rcccx":
            qc.rcccx(gate.qubits[0].index, gate.qubits[1].index, gate.qubits[2].index, gate.qubits[3].index)
        case "rccx":
            qc.rccx(gate.qubits[0].index, gate.qubits[1].index, gate.qubits[2].index)
        case "rv":
            qc.rv(gate.operation.params[0], gate.operation.params[1], gate.operation.params[0], gate.qubits[0].index)
        case "rx":
            qc.rx(gate.operation.params[0], gate.qubits[0].index)
        case "rxx":
            qc.rxx(gate.operation.params[0], gate.qubits[0].index, gate.qubits[1].index)  
        case "ry":
            qc.ry(gate.operation.params[0], gate.qubits[0].index)   
        case "ryy":
            qc.ryy(gate.operation.params[0], gate.qubits[0].index, gate.qubits[1].index)
        case "rz":
            qc.rz(gate.operation.params[0], gate.qubits[0].index)
        case "rzx":
            qc.rzx(gate.operation.params[0], gate.qubits[0].index, gate.qubits[1].index)
        case "rzz":
            qc.rzz(gate.operation.params[0], gate.qubits[0].index, gate.qubits[1].index) 
        case "s":
            qc.s(gate.qubits[0].index)
        case "sdg":
            qc.sdg(gate.qubits[0].index)
        case "swap":
            qc.swap(gate.qubits[0].index, gate.qubits[1].index)
        case "sx":
            qc.sx(gate.qubits[0].index)     
        case "sxdg":
            qc.sxdg(gate.qubits[0].index)
        case "t":
            qc.t(gate.qubits[0].index) 
        case "tdg":
            qc.tdg(gate.qubits[0].index)
        case "u":
            qc.u(gate.operation.params[0], gate.operation.params[1], gate.operation.params[2], gate.qubits[0].index)                     
        case "x":
            qc.x(gate.qubits[0].index)
        case "y":
            qc.y(gate.qubits[0].index)
        case "z":
            qc.z(gate.qubits[0].index)
        case _:
            raise InvalidGateError
            
    return qc

def process_circuit_received(code_string):
    """
    Takes Qiskit code received from frontend, runs it in a temp file, and turns it into a QuantumCircuit

    Args:
        qc_string (String): Qiskit code from frontend

    Returns:
        QuantumCircuit: the QuantumCircuit created by the code given

    """

    # Format code string before running code
    code_lines = code_string.split('\n')
    code_string_formatted = ""
    end_of_imports_found = False

    for i in range(0, len(code_lines)):
        if not end_of_imports_found and "import numpy as np" in code_lines[i]:
            code_string_formatted = code_string_formatted + code_lines[i] + "\ndef main():\n"
            end_of_imports_found = True
        elif end_of_imports_found:
            code_string_formatted = code_string_formatted + "   " + code_lines[i]  + "\n"
        else:
            code_string_formatted = code_string_formatted + code_lines[i] + "\n"

    code_string_formatted = code_string_formatted + "   " + "print([qc.num_qubits, qc.data])" + "\nmain()"

    # Run code in temp file and return QuantumCircuit
    gates = []
    num_qubits = 0

    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
        temp_file.write(code_string_formatted.encode('utf-8'))
        temp_file_name = temp_file.name
    try:
        result = subprocess.run([sys.executable, temp_file_name], capture_output=True, text=True, timeout=5)
        output = eval(result.stdout)

        num_qubits, gates = output[0], output[1]
    except Exception as e:
        raise InputError
    finally:

        # Ensure the temporary file is deleted after execution
        os.remove(temp_file_name)

    # Create QuantumCircuit to return
    print("about to make circuit")
    print(num_qubits, "used")
    qc = QuantumCircuit(num_qubits)
    print("after making circuit")
    for i in range(0, len(gates)):
        apply_gate_to_circuit(qc, gates[i])

    print(qc)

    return qc

def group_gates(num_qubits, qc, little_endian=False):
    """
    Groups gates of quantum circuit into sub arrays. These arrays are used for column visualizations and state calculations.

    Args:
        num_qubits (int): the number of qubits in the circuit
        qc (QuantumCircuit): the quantum circuit being operated on
        little_endian (boolean): whether gates should be grouped for little endian calculations or not

    Returns:
        list[object]: the sorted gates and descriptors explaining multi-Qubit gate behaviour

    Raises:
        InputError: If incorrect formatting used in code given.
    """
    gates = qc.data

    columns = [[[] for i in range(0, num_qubits)]]
    column_pointer = 0


    # Iterate through all gates
    while len(gates) > 0:
        gate = gates.pop(0)
        gate_indices = notation.get_list_of_qubit_indices_in_gate(gate)
        available = True

        # Go through all qubits used in gate
        for i in range(0, len(gate_indices)):

            # If a qubit in the current gate column already is being used for a gate, flag availability as false
            if columns[column_pointer][gate_indices[i]] != []:
                available = False
        
        # Move to the next column if space is not available in current column
        if not available:
            column_pointer = column_pointer + 1
            #if column_pointer >= len(columns):
            columns.append([[] for j in range(0, num_qubits)])

        # Place gate in column
        for i in range(0, len(gate_indices)):
            if i == 0:
                columns[column_pointer][gate_indices[i]] = gate
            else:
                columns[column_pointer][gate_indices[i]] = "MARKED"

    # If little_endian flag, flip all columns
    if little_endian:
        for i in range(0, len(columns)):
            columns[i].reverse()

    return columns