import copy
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

import matrices.matrix_info_registry
from . import Parser, HigherIndexedControlQubitError, GateInformation
from .parser_utils import  get_control_and_target_qubit_indices, insert_main_function_into_code_string, get_qiskit_gate_object_from_gate_name, QISKIT_CIRCUIT_GATE_LOOP, NUMPY_IMPORT_STRING, MAX_NUM_QUBITS_FOR_TENSOR, MAX_NUM_QUBITS_FOR_APP
from matrices.multi_qubit_matrix_information import MultiQubitMatrixInformation

class QiskitParser(Parser):

    def run_pipeline(self, data):
        num_qubits, gate_attributes = self.convert_code_string_to_circuit_object(data)
        gate_information_list = self.create_gate_information_list_for_gates(gate_attributes)
        print("GATE INFORMATION LIST", gate_information_list)
        print(num_qubits, type(num_qubits))

        grouped_gates_big_endian, grouped_gates_little_endian = self.group_gates(num_qubits, gate_information_list)

        matrix_gate_little_endian = self.create_matrix_gate_json(num_qubits, grouped_gates_little_endian)
        matrix_gate_big_endian = self.create_matrix_gate_json(num_qubits, grouped_gates_big_endian, False)

        print("le", matrix_gate_little_endian)
        print("be", matrix_gate_big_endian)

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

        # 5.0. Create data for equation and state parts of circuit and Dirac components
        circuit_dirac_gate_little_endian = self.create_circuit_dirac_gates_json(
            num_qubits, grouped_gates_little_endian
        )
        circuit_dirac_gate_big_endian = self.create_circuit_dirac_gates_json(
            num_qubits, grouped_gates_big_endian
        )

        dirac_state_vector_little_endian = (
            self.format_matrix_state_for_dirac_state_json(
                num_qubits, matrix_state_little_endian
            )
        )
        dirac_state_vector_big_endian = (
            self.format_matrix_state_for_dirac_state_json(
                num_qubits, matrix_state_big_endian
            )
        )

    def convert_code_string_to_circuit_object(code_string):
        code_string = insert_main_function_into_code_string(NUMPY_IMPORT_STRING, code_string, QISKIT_CIRCUIT_GATE_LOOP)
        return super().convert_code_string_to_circuit_object(code_string)
    
    def create_gate_information_list_for_gates(self, gate_attributes):
        gate_information_list = []
        for gate in gate_attributes:
            name = gate["name"]
            qubit_indices = gate["qubit_indices"]
            params = gate["params"]
            control_qubit_indices, target_qubit_indices = (
                get_control_and_target_qubit_indices(name, qubit_indices)
            )

            for control_qubit_index in control_qubit_indices:
                if any(target_qubit_index < control_qubit_index for target_qubit_index in target_qubit_indices):
                    raise HigherIndexedControlQubitError()

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

            matrix = Operator(qc_temp).data

            new_gate_information = GateInformation(
                    name,
                    matrix,
                    len(qubit_indices),
                    control_qubit_indices,
                    target_qubit_indices,
                    params,
                )

            gate_information_list.append(new_gate_information)

        return gate_information_list

    def group_gates(self, num_qubits, gate_information_list):
        return super().group_gates(num_qubits, gate_information_list)

    def create_matrix_gate_json(self, num_qubits, grouped_gates, little_endian=True):
        return super().create_matrix_gate_json(num_qubits, grouped_gates, little_endian)
    
    def create_matrix_state_vector_json(self, num_qubits, matrices):
        return super().create_matrix_state_vector_json(num_qubits, matrices)

    def create_tensor_product_matrix_gate_json(self, num_qubits, grouped_gates, little_endian=True):
        return super().create_tensor_product_matrix_gate_json(num_qubits, grouped_gates, little_endian)

    def create_circuit_dirac_gates_json(self, num_qubits, grouped_gates):
        super().create_circuit_dirac_gates_json(num_qubits, grouped_gates)
        
    def format_matrix_state_for_dirac_state_json(self, num_qubits, state_vector):
        return super().format_matrix_state_vectors_for_dirac_state_json(num_qubits, state_vector)