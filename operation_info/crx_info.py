import numpy as np
import math
import cmath
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CRXInfo(MultiQubitMatrixInformation):
    names = ["crx", "controlled-rotational-x", "controlled-rx"]

    def get_big_endian(self, params):
        theta = params.theta
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, math.cos(theta/2), -1j * math.sin(theta / 2)],
                                [0.+0.j, 0.+0.j, -1j * math.sin(theta / 2), math.cos(theta/2)]], dtype=complex)

    def get_little_endian(self, params):
        theta = params.theta
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, math.cos(theta/2), 0.+0.j, -1j * math.sin(theta / 2)],
                                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                                [0.+0.j,  -1j * math.sin(theta / 2),0.+0.j, math.cos(theta/2)]], dtype=complex)