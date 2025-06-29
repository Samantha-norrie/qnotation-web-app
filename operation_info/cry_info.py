import numpy as np
import math
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CRYInfo(MultiQubitMatrixInformation):
    names = ["cry", "controlled-rotational-y", "controlled-ry"]

    def get_big_endian(self, params):
        theta = params.theta
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, 0.+0.j, math.cos(theta/2), -math.sin(theta / 2)],
                                [0.+0.j, 0.+0.j, math.sin(theta / 2), math.cos(theta/2)]], dtype=complex)

    def get_little_endian(self, params):
        theta = params.theta
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                                [0.+0.j, math.cos(theta/2), 0.+0.j, -math.sin(theta / 2)],
                                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                                [0.+0.j,  math.sin(theta / 2),0.+0.j, math.cos(theta/2)]], dtype=complex)