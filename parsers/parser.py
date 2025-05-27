from abc import ABC, abstractmethod
class Parser(ABC):

    @abstractmethod
    def run_pipeline(data):
        pass

    @abstractmethod
    def convert_code_string_to_circuit_object(code_string):
        pass

    @abstractmethod
    def group_gates():
        pass

    @abstractmethod
    def create_matrix_gate_json():
        pass

    @abstractmethod
    def create_matrix_state_vector_json():
        pass

    @abstractmethod
    def create_tensor_product_matrix_gate_json():
        pass

    @abstractmethod
    def create_circuit_dirac_gates_json():
        pass

    @abstractmethod
    def format_matrix_state_vectors_for_dirac_state_json():
        pass