from . import Parser
from .parser_utils import run_code_string_in_temp_file, QISKIT_CIRCUIT_GATE_LOOP

class QiskitParser(Parser):

    def convert_code_string_to_circuit_object(code_string):
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
            code_string_formatted +  QISKIT_CIRCUIT_GATE_LOOP + "main()\n"
        )

        return run_code_string_in_temp_file(code_string_formatted)


    def group_gates():
        pass
    def create_matrix_gate_json():
        pass
    def create_matrix_state_vector_json():
        pass
    def create_tensor_product_matrix_gate_json():
        pass
    def create_circuit_dirac_gates_json():
        pass
    def format_matrix_state_vectors_for_dirac_state_json():
        pass