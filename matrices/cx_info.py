import numpy as np
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CXInfo(MultiQubitMatrixInformation):
    names = ["cx", "cnot", "⊕", "controlled-x"]

    @classmethod
    def get_big_endian(cls):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)

    @classmethod
    def get_little_endian(cls):
        return np.array([
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0]
        ], dtype=complex)