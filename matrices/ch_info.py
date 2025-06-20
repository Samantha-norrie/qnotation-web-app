import numpy as np
from .multi_qubit_matrix_information import MultiQubitMatrixInformation
from .multi_qubit_matrix_utils import SQRT2_INV

class CHInfo(MultiQubitMatrixInformation):
    names = ["ch", "controlled-hadamard"]

    def get_big_endian(self):
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 0.+0.j, SQRT2_INV, SQRT2_INV],
                [0.+0.j, 0.+0.j, SQRT2_INV, -SQRT2_INV]], dtype=complex)

    def get_little_endian(self):
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, SQRT2_INV, 0.+0.j, SQRT2_INV],
                [0.+0.j, 0.+0.j, SQRT2_INV, 0.+0.j],
                [0.+0.j, SQRT2_INV, 0.+0.j, -SQRT2_INV]], dtype=complex)