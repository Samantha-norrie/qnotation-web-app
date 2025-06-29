import numpy as np
import math
import cmath
from .multi_qubit_matrix_information import MultiQubitMatrixInformation

class CUInfo(MultiQubitMatrixInformation):
    names = ["cu", "controlled-u"]

    def get_big_endian(self, params):
        theta = params.theta
        phi = params.phi
        lam = params.lam
        gamma = params.gamma
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, 1.+0.j, 0.+0.j,  0.+0.j],
                [0.+0.j, 0.+0.j, cmath.exp(1j * gamma) * math.cos(theta / 2), -cmath.exp(1j * (lam+ gamma)) * math.sin(theta / 2)],
                [0.+0.j,  0.+0.j, cmath.exp(1j * (phi+ gamma)) * math.sin(theta / 2), cmath.exp(1j * (phi + lam+ gamma)) * math.cos(theta / 2)]], dtype=complex)

    def get_little_endian(self, params):
        theta = params.theta
        phi = params.phi
        lam = params.lam
        gamma = params.gamma
        return np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                [0.+0.j, cmath.exp(1j * gamma) * math.cos(theta / 2), 0.+0.j,  -cmath.exp(1j * (lam+ gamma)) * math.sin(theta / 2)],
                [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                [0.+0.j,  cmath.exp(1j * (phi+ gamma)) * math.sin(theta / 2), 0.+0.j, cmath.exp(1j * (phi + lam+ gamma)) * math.cos(theta / 2)]], dtype=complex)