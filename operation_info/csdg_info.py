import numpy as np
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CSDGInfo(MultiQubitMatrixInformation):
    names = ["csdg", "controlled-s-dagger"]

    def get_big_endian(self):
        return np.array([
        [1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
        [0.+0.j, 0.+0.j, 0.+0.j, -1j]],  dtype=complex)

    def get_little_endian(self):
        return np.array([
        [1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
        [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
        [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
        [0.+0.j, 0.+0.j, 0.+0.j, -1j]],  dtype=complex)