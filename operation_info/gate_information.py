import numpy as np

class GateInformation:

    def __init__(
        self,
        name: str,
        matrix_be: np.ndarray,
        matrix_le: np.ndarray,
        num_qubits: int,
        control_qubit_indices: list[int],
        target_qubit_indices: list[int] = [],
        params=[],
    ) -> None:

        self._name = name
        self._matrix_be = matrix_be
        self._matrix_le = matrix_le
        self._num_qubits = num_qubits
        self._control_qubit_indices = control_qubit_indices
        self._target_qubit_indices = target_qubit_indices
        self._params = params

    def __str__(self): 
        return f"GateInformation(name='{self._name}', matrix_be={self._matrix_be}, matrix_le={self._matrix_le}, num_qubits={self._num_qubits}, control_qubit_indices={self._control_qubit_indices}, target_qubit_indices={self._target_qubit_indices}, params={self._params} )"
    
    def __repr__(self):
        return self.__str__()

    def get_name(self) -> str:
        return self._name

    def get_matrix_be(self) -> np.ndarray:
        return self._matrix_be
    
    def get_matrix_le(self) -> np.ndarray:
        return self._matrix_le

    def get_num_qubits(self) -> int:
        return self._num_qubits

    def get_control_qubit_indices(self) -> list[int]:
        return self._control_qubit_indices

    def get_target_qubit_indices(self) -> list[int]:
        return self._target_qubit_indices

    def get_params(self):
        return self._params
