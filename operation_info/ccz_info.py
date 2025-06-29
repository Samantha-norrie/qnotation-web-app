import numpy as np
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CCZInfo(MultiQubitMatrixInformation):
    names = ["ccz", "controlled-controlled-z"]

    def get_big_endian(self):
        return np.array([
    [1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 1+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 1+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 1+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 1+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, -1+0j],
], dtype=complex)

    def get_little_endian(self):
        return np.array([
    [1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 1+0j, 0+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 1+0j, 0+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 1+0j, 0+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 1+0j, 0+0j],
    [0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, -1+0j],
], dtype=complex)