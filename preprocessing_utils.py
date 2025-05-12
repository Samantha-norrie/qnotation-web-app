from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit.circuit import CircuitInstruction, Instruction, Qubit, QuantumRegister
from qiskit.circuit.library import HGate
from errors import InvalidGateError, InputError
import subprocess
import copy
import sys
import os
import tempfile
from GateInformation import GateInformation
from utils import *
from errors import *


def create_gate_information_list_for_gates(attributes_for_gates):
    """
    Creates GateInformation objects representing each gate in the given QuantumCircuit object

    Args:
        qc (QuantumCircuit): the quantum circuit to be turned into GateInformation objects

    Returns:
        list[GateInformation]: a list of the created GateInformation objects
    """
    gate_information_list = []

    for gate in attributes_for_gates:
        name = gate["name"]
        qubit_indices = gate["qubit_indices"]
        params = gate["params"]
        control_qubit_indices, target_qubit_indices = (
            get_control_and_target_qubit_indices(name, qubit_indices)
        )

        # Transform gate into a matrix (workaround for Qiskit 1.3)
        sorted_qubit_indices = copy.deepcopy(qubit_indices)
        sorted_qubit_indices.sort()

        gate_qubit_size = (
            1
            if len(qubit_indices) == 1
            else sorted_qubit_indices[len(sorted_qubit_indices) - 1]
            + 1
            - sorted_qubit_indices[0]
        )
        qc_temp = QuantumCircuit(gate_qubit_size)
        qc_temp.append(
            get_gate_object_from_gate_name(name, params),
            [i for i in range(0, gate_qubit_size)],
        )

        matrix = Operator(qc_temp).data

        # Create GateInformation object and appending it to list
        gate_information_list.append(
            GateInformation(
                name,
                matrix,
                len(qubit_indices),
                control_qubit_indices,
                target_qubit_indices,
                params,
            )
        )

    return gate_information_list


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


def process_circuit_received(code_string):
    """
    Takes Qiskit code received from frontend, runs it in a temp file, and turns it into a QuantumCircuit

    Args:
        qc_string (String): Qiskit code from frontend

    Returns:
        QuantumCircuit: the QuantumCircuit created by the code given
    """

    # Format code string before running code
    code_lines = code_string.split("\n")
    code_string_formatted = ""
    end_of_imports_found = False

    for i in range(0, len(code_lines)):
        if not end_of_imports_found and "import numpy as np" in code_lines[i]:
            code_string_formatted = (
                code_string_formatted + code_lines[i] + "\ndef main():\n"
            )
            end_of_imports_found = True
        elif end_of_imports_found:
            code_string_formatted = code_string_formatted + "    "+ code_lines[i] + "\n"
        else:
            code_string_formatted = code_string_formatted + code_lines[i] + "\n"\

    code_string_formatted = (
        code_string_formatted +  CIRCUIT_GATE_LOOP + "main()\n"
    )

    print("CODE STRING FORMATTED", code_string_formatted)

    # Run code in temp file and return QuantumCircuit

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code_string_formatted.encode("utf-8"))
        temp_file_name = temp_file.name
    try:
        result = subprocess.run(
            [sys.executable, temp_file_name], capture_output=True, text=True, timeout=5
        )
        print("ERR", result.stderr)
        output = eval(result.stdout)


    except Exception as e:
        print("input error caught in process_circuit_received:", e)
        raise InputError
    finally:

        # Ensure the temporary file is deleted after execution
        os.remove(temp_file_name)

    return output


def group_gates(num_qubits, gates_and_indices):
    """
    Groups gates of quantum circuit into sub arrays. These arrays are used for column visualizations and state calculations.

    Args:
        num_qubits (int): the number of qubits in the circuit
        gates_and_indices (list[GateInformation]): list of GateInformation objects representing the quantum circuit

    Returns:
        list[object]: the sorted gates and descriptors explaining multi-Qubit gate behaviour

    Raises:
        InputError: If incorrect formatting used in code given.
    """

    column = [NOT_INVOLVED for i in range(0, num_qubits)]
    grouped_gates_be = [copy.deepcopy(column)]
    column_pointer = 0

    # Iterate through all gates
    while len(gates_and_indices) > 0:
        gate = gates_and_indices.pop(0)

        control_qubit_indices = gate.get_control_qubit_indices()
        target_qubit_indices = gate.get_target_qubit_indices()

        all_gate_indices = control_qubit_indices + target_qubit_indices

        available = True

        # Go through all qubits used in gate
        for i in range(0, len(all_gate_indices)):

            # If a qubit in the current gate column already is being used for a gate, flag availability as false
            if grouped_gates_be[column_pointer][all_gate_indices[i]] != NOT_INVOLVED:
                available = False

        # Move to the next column if space is not available in current column
        if not available:
            column_pointer = column_pointer + 1
            grouped_gates_be.append(copy.deepcopy(column))

        # Place gate in column

        # If single-qubit gate, place CircuitInstruction
        if len(all_gate_indices) == 1:
            grouped_gates_be[column_pointer][all_gate_indices[0]] = gate

        # if multi-qubit gate, place control and target qubits
        else:

            # Place control qubits
            for j in range(0, len(control_qubit_indices)):

                # Place CircuitInstruction at first control index
                if j == 0:
                    grouped_gates_be[column_pointer][control_qubit_indices[j]] = gate
                else:
                    grouped_gates_be[column_pointer][control_qubit_indices[j]] = CONTROL

            # Place target qubits
            for j in range(0, len(target_qubit_indices)):
                grouped_gates_be[column_pointer][target_qubit_indices[j]] = TARGET

            # Mark auxiliary qubits
            min_control = min(control_qubit_indices)
            min_target = min(target_qubit_indices)
            min_index = min_target if min_target < min_control else min_control

            max_control = max(control_qubit_indices)
            max_target = max(target_qubit_indices)
            max_index = max_target if max_target > max_control else max_control

            start_of_gate_found = False
            for j in range(min_index, max_index):
                if (
                    not start_of_gate_found
                    and grouped_gates_be[column_pointer][j] != NOT_INVOLVED
                ):
                    start_of_gate_found = True
                elif start_of_gate_found:
                    if grouped_gates_be[column_pointer][j] == NOT_INVOLVED:
                        grouped_gates_be[column_pointer][j] = AUXILIARY
                    else:
                        break

    # Create grouped gates for little endian formatting
    grouped_gates_le = copy.deepcopy(grouped_gates_be)
    for i in range(0, len(grouped_gates_le)):
        grouped_gates_le[i].reverse()

    return grouped_gates_be, grouped_gates_le
