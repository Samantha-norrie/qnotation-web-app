from qiskit.quantum_info.operators import Operator
import numpy as np

class Notation:

    # Create list of grouped gates which can be used for circuit and Dirac display
    def create_circuit_dirac_gates_json(num_qubits, operation_list):
        circuit_json_list = []

        circuit_json_list.append({"content": [[0] for i in range(0, num_qubits)], "type": "QUBIT","key": 0})

        for i in range(0, len(operation_list)):
            content = []
            for j in range(0, num_qubits):
                if j < len(operation_list[i]):
                    content.append({"gate": operation_list[i][j].operation.name})
                else:
                    content.append({"gate": None})

            circuit_json_list.append({"content": content, "type": "GATE","key": i+1})

        return circuit_json_list

   # Create list of state vectors for matrix display
    def create_matrix_state_vector_json(num_qubits, matrices=[]):

        matrix_vector_state_json = []

        vector = np.array([[1 if i == 0 else 0] for i in range(0, 2**num_qubits)])
        matrix_vector_state_json.append({"content": vector.tolist(), "type": "STATE","key": 0})

        for i in range(0, len(matrices)):
            vector = np.dot(matrices[i]["content"], vector)

            matrix_vector_state_json.append({"content": vector.tolist(), "type": "GATE","key": i+1})

        return matrix_vector_state_json
    
    def simplify_values(matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                real_val = float(matrix[i][j].real)
                imag_val = float(matrix[i][j].imag)
                print(type(real_val) , real_val)
                print(type(imag_val) , imag_val)

                if real_val == 0.0 and imag_val == 0.0:
                    matrix[i][j] = 0.0
                elif imag_val == 0.0:
                    
                    matrix[i][j] = float(round(real_val,2))
                    print("in here", type(matrix[i][j]))

        return matrix


    # Create list of matrices of grouped gates which can be used matrix display
    def create_matrix_gate_json(num_qubits, operation_list):

        matrix_gate_json_list = []

        # identity_matrix = np.array([[1 if i == j else 0 for j in range(2**num_qubits)] for i in range(2**num_qubits)])

        # matrix_gate_json_list.append({"content": identity_matrix.tolist(), "type": "INIT","key": 0})


        for i in range(0, len(operation_list)):

            matrix = Operator(operation_list[i][0].operation).data
            for j in range(1, len(operation_list[i])):
                matrix = np.kron(matrix, Operator(operation_list[i][j].operation).data)

            matrix_gate_json_list.append({"content": Notation.simplify_values(matrix.tolist()), "type": "GATE","key": i+1})

        # Notation.simplify_values(matrix_gate_json_list)
        return matrix_gate_json_list

    def create_matrix_gate_json_with_tensor_product(num_qubits, operation_list):  
        matrix_gate_json_list = []

        # identity_matrix = np.array([[1 if i == j else 0 for j in range(2**num_qubits)] for i in range(2**num_qubits)])

        # matrix_gate_json_list.append({"content": identity_matrix.tolist(), "type": "INIT","key": 0})


        for i in range(0, len(operation_list)):

            matrices = []
            min_qubit = num_qubits
            max_qubit = 0

            # matrix = Operator(operation_list[i][0].operation).data
            for j in range(0, len(operation_list[i])):
                # matrix = np.kron(matrix, Operator(operation_list[i][j].operation).data)
                matrices.append(Notation.simplify_values(Operator(operation_list[i][0].operation).data))

            matrix_gate_json_list.append({"content": matrices, "type": "GATE","key": i+1})

        # Notation.simplify_values(matrix_gate_json_list)
        return matrix_gate_json_list

    def group_gates(circuit):
        gates = circuit.data

        operation_list = []
        operation = []
        qubits_in_operation = []

        while len(gates) > 0:
            current_gate = gates.pop(0)

            qubit_overlap = False
            for k in range(0, len(current_gate.qubits)):
                if current_gate.qubits[k] in qubits_in_operation:
                    qubit_overlap = True
                    break
            
            if qubit_overlap:
                operation_list.append(operation)
                operation = []
                qubits_in_operation = []

            operation.append(current_gate)
            qubits_in_operation.extend(current_gate.qubits)

        if len(operation) > 0:
            operation_list.append(operation)

        return operation_list



