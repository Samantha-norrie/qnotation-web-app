# QNotation

[QNotation](https://qnotation.vercel.app/) is a web application designed to help users convert between circuit, Dirac, and matrix notation in the context of quantum computing.
## Workflow
QNotation is available at [https://qnotation.vercel.app/](https://qnotation.vercel.app/), so no setup is required! This section walks you through running your quantum circuits in the app.

### 1. Inputting your quantum circuit into QNotation
QNotation takes in [Qiskit](https://www.ibm.com/quantum/qiskit) [quantum circuit objects](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.QuantumCircuit), which are inputted through the code editor on the right side of the app.
Here are some points to keep in mind while creating your quantum circuits for QNotation:
- quantum gates must be appended to the ```qc``` variable below the ```Insert code below``` comment. 
- quantum circuits with 1 to 5 qubits can be run in the app. To change the number of qubits used in your circuit, modify the qubit argument on the following line: ```qc = QuantumCircuit(3)```
- measurement and classical operations are currently not supported
- Neighbouring qubits must be used for multi-qubit gates.
  - ✅ ```qc.cx(0, 1)```
  - ❌ ```qc.cx(0, 2)```
- Control qubit(s) must have a lower qubit index than their respective target(s)
  - ✅ ```qc.cx(0, 1)```
  - ❌ ```qc.cx(1, 0)```
- most Qiskit gates are supported by the app. A list of supported gates can be found below

Example input can be found in the *EXAMPLES* dropdown.

### 2. Interpreting notation data
QNotation contains interactive visualizations for circuit, Dirac, and matrix. Clicking on different sections of a notation will reveal its equivalent sections in the other notations (in orange). The quantum state after the selected sections is shown on the right of the Dirac and matrix visualization subsections.

#### 2.1 Additional features for exploring 
A couple of toggles have been included on the bottom right of the app:
- **Little endian (LE) toggle**: allows for toggling between little endian and big endian ordering
- **Tensor (⊗) toggle**: allows matrix notation visualization to be broken down into tensor products (for quantum circuits with 3 qubits or less)

## Publications
- Samantha Norrie, Anthony Estey, Hausi Müller, Ulrike Stege, [QNotation: A Visual Browser-Based Notation Translator for Learning Quantum Computing](https://ieeexplore.ieee.org/document/10821137), technical paper published in the proceedings of QSEEC 2024 (QCE 2024)
- Samantha Norrie, Anthony Estey, [QNotation: An Interactive Visual Tool to Lower Learning Barriers in Quantum Computing](https://ieeexplore.ieee.org/document/10313602), extended abstract and poster published in QCE 2023 –*Jupyter notebook version*

## Disclaimer
QNotation is currently in **beta**. Although it has been tested, it may still contain bugs or unexpected behaviour.

### Qiskit Gates Supported by QNotation
- [CCX: Controlled-controlled-x (Toffoli) gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CCXGate)
- [CCZ: Controlled-controlled-z gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CCZGate)
- [CH: Controlled-hadamard gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CHGate)
- [CP: Controlled-phase gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CPhaseGate)
- [CRX: Controlled-rx gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CRXGate)
- [CRZ: Controlled-rx gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CRZGate)
- [CSDG: Controlled-s^dagger gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CSdgGate)
- [CS: Controlled-s gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CSGate)
- [CU: Controlled-u gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CUGate)
- [CX: Controlled-x gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CXGate)
- [CZ: Controlled-z gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.CZGate)
- [H: Hadamard gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.HGate)
- [ID: Identity gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.IGate)
- [RCCX: Margolous gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.RCCXGate)
- [R: Rot gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.RGate)
- [RX: Rot-x gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.RXGate)
- [RY: Rot-y gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.RYGate)
- [RZ: Rot-z gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.RZGate)
- [X: Pauli-x gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.XGate)
- [Y: Pauli-y gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.YGate)
- [Z: Pauli-Z gate](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.ZGate)
