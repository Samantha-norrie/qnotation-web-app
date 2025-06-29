import copy
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from . import Parser
from operation_info.gate_information import GateInformation
from errors.errors import HigherIndexedControlQubitError, NonNeighbouringQubitsError, TooManyQubitsError
from .parser_utils import  get_control_and_target_qubit_indices, insert_main_function_into_code_string, get_qiskit_gate_object_from_gate_name, QISKIT_CIRCUIT_GATE_LOOP, NUMPY_IMPORT_STRING, MAX_NUM_QUBITS_FOR_TENSOR, MAX_NUM_QUBITS_FOR_APP
from operation_info.multi_qubit_matrix_information import MultiQubitMatrixInformation

class QiskitParser(Parser):

    def run_pipeline(self, qc_string):
        """
        Runs pipeline for generating visualizations from Qiskit code

        Args:
            qc_string (str): Qiskit code as a string

        Returns:
            dict[object]: data needed for visualizations
        """
        num_qubits, gate_attributes = self.convert_code_string_to_circuit_object(qc_string)

        if num_qubits > MAX_NUM_QUBITS_FOR_APP:
            raise TooManyQubitsError()

        gate_information_list = self.create_gate_information_list_for_gates(gate_attributes)

        grouped_gates_big_endian, grouped_gates_little_endian = self.group_gates(num_qubits, gate_information_list)

        matrix_gate_little_endian = self.create_matrix_gate_json(num_qubits, grouped_gates_little_endian)
        matrix_gate_big_endian = self.create_matrix_gate_json(num_qubits, grouped_gates_big_endian, False)

        matrix_state_little_endian = self.create_matrix_state_vector_json(num_qubits, matrix_gate_little_endian)

        matrix_state_big_endian = self.create_matrix_state_vector_json(num_qubits, matrix_gate_big_endian)

        if num_qubits <= MAX_NUM_QUBITS_FOR_TENSOR:
            matrix_gate_tensor_little_endian = self.create_tensor_product_matrix_gate_json(
                num_qubits, grouped_gates_little_endian, True
            )
            matrix_gate_tensor_little_endian.insert(
                0, matrix_state_little_endian[0]
            )

            matrix_gate_tensor_big_endian = self.create_tensor_product_matrix_gate_json(
                num_qubits, grouped_gates_big_endian
            )
            matrix_gate_tensor_big_endian.insert(0, matrix_state_big_endian[0])

        matrix_gate_little_endian = self.simplify_matrices_json(matrix_gate_little_endian)
        matrix_gate_big_endian = self.simplify_matrices_json(matrix_gate_big_endian)

        matrix_gate_little_endian.insert(0, matrix_state_little_endian[0])
        matrix_gate_big_endian.insert(0, matrix_state_big_endian[0])

        circuit_dirac_gate_little_endian = self.create_circuit_dirac_gates_json(
            num_qubits, grouped_gates_little_endian
        )
        circuit_dirac_gate_big_endian = self.create_circuit_dirac_gates_json(
            num_qubits, grouped_gates_big_endian
        )

        dirac_state_little_endian = (
            self.format_matrix_state_for_dirac_state_json(
                num_qubits, matrix_state_little_endian
            )
        )
        dirac_state_big_endian = (
            self.format_matrix_state_for_dirac_state_json(
                num_qubits, matrix_state_big_endian
            )
        )

        return {
            "matrix_gate_little_endian": matrix_gate_little_endian,
            "matrix_gate_big_endian": matrix_gate_big_endian,
            "matrix_gate_tensor_little_endian": matrix_gate_tensor_little_endian,
            "matrix_gate_tensor_big_endian": matrix_gate_tensor_big_endian,
            "matrix_state_little_endian": matrix_state_little_endian,
            "matrix_state_big_endian": matrix_state_big_endian,
            "circuit_dirac_gate_little_endian": circuit_dirac_gate_little_endian,
            "circuit_dirac_gate_big_endian": circuit_dirac_gate_big_endian,
            "dirac_state_little_endian": dirac_state_little_endian,
            "dirac_state_big_endian": dirac_state_big_endian,
            "num_qubits": num_qubits,
            "message": "",
            "status": 200,
        }

    def convert_code_string_to_circuit_object(self, qc_string):
        """
        Adds code for retrieving data from original qc_string and calls convert_code_string_to_circuit_object

        Args:
            qc_string (str): Qiskit code as a string

        Returns:
            list[int, Unknown]: list containing the number of qubits in the circuit and information about its gates
        """
        qc_string = insert_main_function_into_code_string(NUMPY_IMPORT_STRING, qc_string, QISKIT_CIRCUIT_GATE_LOOP)
        return super().convert_code_string_to_circuit_object(qc_string)
    
    def create_gate_information_list_for_gates(self, gate_attributes):
        """
        Creates GateInformation using gate attributes extracted from code

        Args:
            gate_attributes (list[Unknown]): Qiskit gate details

        Returns:
            list[GateInformation]: list containing GateInformation objects describing the given circuit
        """
        gate_information_list = []
        for gate in gate_attributes:
            name = gate["name"]
            qubit_indices = gate["qubit_indices"]
            params = gate["params"]
            control_qubit_indices, target_qubit_indices = (
                get_control_and_target_qubit_indices(name, qubit_indices)
            )

            for control_qubit_index in control_qubit_indices:
                for target_qubit_index in target_qubit_indices:
                    if control_qubit_index > target_qubit_index:
                        raise HigherIndexedControlQubitError()
                
            sorted_control_target_list = control_qubit_indices + target_qubit_indices
            for i in range(0, len(sorted_control_target_list)-1):
                if sorted_control_target_list[i+1] - sorted_control_target_list[i] > 1:
                    raise NonNeighbouringQubitsError()

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
                get_qiskit_gate_object_from_gate_name(name, params),
                [i for i in range(0, gate_qubit_size)],
            )

            num_qubits = len(qubit_indices)
            matrix_le = Operator(qc_temp).data

            matrix_be = matrix_le if num_qubits == 1 else (MultiQubitMatrixInformation.get_gate_class(name)).get_big_endian()

            new_gate_information = GateInformation(
                    name,
                    matrix_be,
                    matrix_le,
                    num_qubits,
                    control_qubit_indices,
                    target_qubit_indices,
                    params,
                )

            gate_information_list.append(new_gate_information)

        return gate_information_list