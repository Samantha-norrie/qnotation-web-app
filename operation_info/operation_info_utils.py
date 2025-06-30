import numpy as np
from quantum_library_parsers.parser_utils import GateNames

SQRT2_INV= 1 / np.sqrt(2)

gate_aliases = {
    GateNames.CONTROLLED_CONTROLLED_X.value: ["ccx", "controlled-controlled-x", "CCNOT"],
    GateNames.CONTROLLED_CONTROLLED_Z.value: ["ccz", "controlled-controlled-z"],
    GateNames.CONTROLLED_HADAMARD.value: ["ch", "controlled-hadamard"],
    GateNames.CONTROLLED_PHASE.value: ["cp", "controlled-phase"],
    GateNames.CONTROLLED_ROTAIONAL_X.value: ["crx", "controlled-rotational-x", "controlled-rotational-not"],
    GateNames.CONTROLLED_ROTAIONAL_Z.value: ["crz", "controlled-rotational-Z"],
    GateNames.CONTROLLED_S_DAGGER.value: ["csdg", "controlled-s-dagger"],
    GateNames.CONTROLLED_S.value: ["cs", "controlled-s"],
    GateNames.CONTROLLED_U.value: ["cu", "controlled-u", "controlled-unitary"],
    GateNames.CONTROLLED_X.value: ["cx", "cnot", "controlled-not", "controlled-x"],
    GateNames.CONTROLLED_Z.value: ["cy", "controlled-y"],
    GateNames.CONTROLLED_Z.value: ["cz", "controlled-z"],
    GateNames.HADAMARD.value: ["h", "hadamard"],
    GateNames.IDENTITY.value: ["i", "id", "identity"],
    GateNames. RELATIVE_PHASE_CONTROLLED_CONTROLLED_X.value: ["rccx", "margolous", "simplified-toffoli"],
    GateNames.ROTATIONAL.value: ["r", "rot", "rotational"],
    GateNames.ROTATIONAL_X.value: ["rx", "rot-x", "rotational-x", "rotational-not"],
    GateNames.ROTATIONAL_Y.value: ["ry", "rot-y", "rotational-y"],
    GateNames.ROTATIONAL_Z.value: ["rz", "rot-z", "rotational-z"],
    GateNames.X.value: ["x", "not", "pauli-x"],
    GateNames.Y.value: ["y", "pauli-y"],
    GateNames.Z.value: ["z", "pauli-z"]
}

name_to_acronym = {
    name.lower(): acronym
    for acronym, names in gate_aliases.items()
    for name in names
}

def get_gate_acronym(name: str) -> str | None:
    return name_to_acronym.get(name.lower())