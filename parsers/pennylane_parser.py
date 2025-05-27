from . import Parser, HigherIndexedControlQubitError, GateInformation
from .parser_utils import run_code_string_in_temp_file, get_control_and_target_qubit_indices, get_multi_qubit_gate_le, PENNYLANE_CIRCUIT_GATE_LOOP

class PennylaneParser(Parser):
    def run_pipeline(self, data):
        num_qubits, gate_attributes = self.convert_code_string_to_circuit_object(data)
        gate_information_list = self.create_gate_information_list_for_gates()
        grouped_gates_be, grouped_gates_le = self.group_gates(gate_attributes)

    def convert_code_string_to_circuit_object(self, code_string):
        code_string = code_string + PENNYLANE_CIRCUIT_GATE_LOOP
        print(code_string)
        return run_code_string_in_temp_file(code_string)

    def create_gate_information_list_for_gates(self, gate_attributes):
        gate_information_list = []

        for gate in gate_attributes:
            name = gate["name"]
            qubit_indices = gate["wires"]
            params = gate["params"]
            matrix_be = gate["matrix"]
            control_qubit_indices, target_qubit_indices = (
                get_control_and_target_qubit_indices(name, qubit_indices)
            )

            for control_qubit_index in control_qubit_indices:
                if any(target_qubit_index < control_qubit_index for target_qubit_index in target_qubit_indices):
                    raise HigherIndexedControlQubitError()

            num_qubits = len(qubit_indices)
            matrix_le = []
            if num_qubits == 1:
                matrix_le = matrix_be
            else:
                get_multi_qubit_gate_le(name)

            new_gate_information = GateInformation(
                    name,
                    matrix_be,
                    matrix_le,
                    len(qubit_indices),
                    control_qubit_indices,
                    target_qubit_indices,
                    params,
                )

            gate_information_list.append(new_gate_information)

        return gate_information_list
        
    def group_gates(self):
        pass
    def create_matrix_gate_json(self):
        pass
    def create_matrix_state_vector_json(self):
        pass
    def create_tensor_product_matrix_gate_json(self):
        pass
    def create_circuit_dirac_gates_json(self):
        pass
    def format_matrix_state_vectors_for_dirac_state_json(self):
        pass