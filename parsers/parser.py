from abc import ABC, abstractmethod
import copy
import subprocess
import tempfile
import sys
import os
import copy
import numpy as np
from numpy import array
import pennylane as qml
import cirq

from .parser_utils import NOT_INVOLVED, AUXILIARY, CONTROL, TARGET, GATE, IDENTITY_MATRIX, STATE, GATE_INFO, IDENTITY_MATRIX_NAME, simplify_values_state_vector, simplify_single_matrix
from errors import InputError
from gate_information import GateInformation

class Parser(ABC):

    @abstractmethod
    def run_pipeline(self, data):
        pass

    @abstractmethod
    def convert_code_string_to_circuit_object(self, code_string):
        """
        Takes code as a string, runs it inside a temp file, and returns what is received from stdout

        Args:
        code_string (String): string of code to be run

        Returns:
            Unknown: what is received from stdout
        """
        print("CODE STRING", code_string)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code_string.encode("utf-8"))
            temp_file_name = temp_file.name
        try:
            result = subprocess.run(
                [sys.executable, temp_file_name], capture_output=True, text=True, timeout=5
            )
            print("ERR", result.stderr)
            print("stdout", result.stdout)
            output = eval(result.stdout, {"qml": qml, "array": array, "cirq": cirq})


        except Exception as e:
            print("input error caught in process_circuit_received:", e)
            raise InputError
        finally:

            # Ensure the temporary file is deleted after execution
            os.remove(temp_file_name)

        return output

    @abstractmethod
    def group_gates(self, num_qubits, gate_information_list):
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
        while len(gate_information_list) > 0:
            gate = gate_information_list.pop(0)

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

    @abstractmethod
    def create_matrix_gate_json(self, num_qubits, grouped_gates, little_endian=True):
        """
        Creates list of JSON objects which contain matrix representations of gate columns, their types (GATE), and their indices

        Args:
            num_qubits (int): the number of qubits in the circuit
            grouped_gates (list[object]): the quantum circuit being operated on

        Returns:
            list[object]: A list of JSON objects representing the given grouped gates in matrix form
        """

        matrix_gate_json_list = []

        # Go through each grouped gate column and check each qubit
        for i in range(0, len(grouped_gates)):

            # Store computed matrix for column in matrix variable
            matrix = []

            for j in range(0, num_qubits):

                current_qubit_in_column = grouped_gates[i][j]

                # Continue if current qubit does not contain a GateInformation object or is involved in a gate
                if (
                    current_qubit_in_column == AUXILIARY
                    or current_qubit_in_column == CONTROL
                    or current_qubit_in_column == TARGET
                ):
                    continue

                # Set matrix to equal identity matrix if no gate has been applied yet and qubit is not involved in any gate
                elif len(matrix) == 0 and current_qubit_in_column == NOT_INVOLVED:
                    matrix = IDENTITY_MATRIX

                # Apply identity matrix to existing matrix if qubit is not involved in any gate
                elif current_qubit_in_column == NOT_INVOLVED:
                    matrix = np.kron(matrix, IDENTITY_MATRIX)

                # If no matrix has been applied yet..
                elif len(matrix) == 0:
                    matrix = current_qubit_in_column.get_matrix_le() if little_endian else current_qubit_in_column.get_matrix_be()

                # If matrices have already been applied...
                else:
                    matrix = np.kron(matrix, current_qubit_in_column.get_matrix_le()) if little_endian else np.kron(matrix, current_qubit_in_column.get_matrix_be())

            matrix_gate_json_list.append(
                {"content": matrix.tolist(), "type": GATE, "key": i + 1}
            )

        return matrix_gate_json_list

    @abstractmethod
    def create_matrix_state_vector_json(self, num_qubits, matrices):
        """
        Creates JSON objects of state vectors representing the state of the quantum circuit at each of its columns

        Args:
            num_qubits (int): the number of qubits in the quantum circuit
            matrices (list[object]): a list of matrices representing the columns in the quantum circuit

        Returns:
            list[object]: list of state vector JSON objects
        """

        matrix_vector_state_json = []

        # Initial state (no gates applied yet) representing all qubits being set to 0
        vector = np.array([[1 if i == 0 else 0] for i in range(0, 2**num_qubits)])

        matrix_vector_state_json.append(
            {"content": vector.tolist(), "type": STATE, "key": 0}
        )

        for i in range(0, len(matrices)):

            vector = np.dot(matrices[i]["content"], vector)
            matrix_vector_state_json.append(
                {
                    "content": simplify_values_state_vector(vector.tolist()),
                    "type": GATE,
                    "key": i + 1,
                }
            )

        return matrix_vector_state_json

    @abstractmethod
    def create_tensor_product_matrix_gate_json(self, num_qubits, grouped_gates, little_endian=False):
        """
        Creates lists of matrices for tensor product setting

        Args:
            num_qubits (int): number of qubits in the circuit
            grouped_gates (list[object]): quantum circuit being operated on
            little_endian (boolean): flag for endianess

        Returns:
            list[object]: list of JSON objects describing matrices for tensor product setting
        """

        matrix_gate_json_list = []

        # Go through each grouped gate column and check each qubit
        for i in range(0, len(grouped_gates)):

            matrices = []

            # Matrix calculations for column
            for j in range(0, num_qubits):

                current_qubit_in_column = grouped_gates[i][j]

                # format and append matrices found to list
                if type(current_qubit_in_column) == GateInformation:

                    matrices.append(
                        simplify_single_matrix(
                            current_qubit_in_column.get_matrix().tolist()
                        ).copy()
                    )

                # append identity matrix if qubit is not being used by any other gate
                elif current_qubit_in_column == NOT_INVOLVED:
                    matrices.append(IDENTITY_MATRIX.tolist())

            matrix_gate_json_list.append({"content": matrices, "type": GATE, "key": i + 1})
        return matrix_gate_json_list

    @abstractmethod
    def create_circuit_dirac_gates_json(self, num_qubits, grouped_gates):
        """
        Creats JSON objects for describing data for equation components for circuit and Dirac

        Args:
            num_qubits (int): the number of qubits in the quantum circuit
            grouped_gates (list[object]): the quantum circuit being operated on

        Returns:
            list[object]: list of JSON objects containing information for circuit and Dirac equation components
        """
        circuit_dirac_gate_json_list = []

        circuit_dirac_gate_json_list.append(
            {"content": [[0] for i in range(0, num_qubits)], "type": STATE, "key": 0}
        )

        # Go through each grouped gate column and check each qubit
        for i in range(0, len(grouped_gates)):

            content = []

            for j in range(0, num_qubits):
                current_qubit_in_column = grouped_gates[i][j]

                if type(current_qubit_in_column) == GateInformation:
                    content.append(
                        {
                            "gate": current_qubit_in_column.get_name().upper(),
                            "gate_type": GATE_INFO,
                        }
                    )
                elif current_qubit_in_column == NOT_INVOLVED:
                    content.append(
                        {"gate": IDENTITY_MATRIX_NAME, "gate_type": current_qubit_in_column}
                    )
                else:
                    content.append({"gate": "", "gate_type": current_qubit_in_column})

            circuit_dirac_gate_json_list.append(
                {"content": content, "type": GATE, "key": i + 1}
            )

        return circuit_dirac_gate_json_list

    @abstractmethod
    def format_matrix_state_for_dirac_state_json(self, num_qubits, state_vector):
        """
        Make Dirac states using matrix state vectors. Only make states that have an amplitude != 0

        Args:
            num_qubits (int): number of qubits in the circuit
            state_vector (list[object]): list of JSON objects describing state vectors

        Returns:
            list[object]: A list of JSON objects representing the given state vectors as Dirac states
        """

        dirac_state_json = []
        format_val = "0" + str(num_qubits) + "b"

        for i in range(0, len(state_vector)):
            values = []
            for j in range(0, len(state_vector[i]["content"])):

                # if the state exists, convert it into binary
                if state_vector[i]["content"][j][0] != 0:
                    values.append(
                        {
                            "bin": format(j, format_val),
                            "scalar": state_vector[i]["content"][j][0],
                        }
                    )
            dirac_state_json.append({"content": values, "type": STATE, "key": i})

        return dirac_state_json
