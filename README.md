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
- most Qiskit gates are supported by the app. A full list of supported gates can be found [here]()

Example input can be found in the *EXAMPLES* dropdown.

### 2. Interpreting notation data

## Publications
- Samantha Norrie, Anthony Estey, Hausi Müller, Ulrike Stege, [QNotation: A Visual Browser-Based Notation Translator for Learning Quantum Computing](https://ieeexplore.ieee.org/document/10821137), technical paper published in the proceedings of QSEEC 2024 (QCE 2024)
- Samantha Norrie, Anthony Estey, [QNotation: An Interactive Visual Tool to Lower Learning Barriers in Quantum Computing](https://ieeexplore.ieee.org/document/10313602), extended abstract and poster published in QCE 2023 –*Jupyter notebook version*

## Disclaimer
QNotation is currently in **beta**. Although it has been tested, it may still contain bugs or unexpected behaviour.
