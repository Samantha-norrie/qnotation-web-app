import numpy as np
import cmath
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CPInfo(MultiQubitMatrixInformation):
    names = ["cp", "controlled-phase"]

    def get_big_endian(self, params):
        phi = params.phi
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * phi)]], dtype=complex)

    def get_little_endian(self, params):
        phi = params.phi
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, 0.+0.j, cmath.exp(1j * phi)]], dtype=complex)