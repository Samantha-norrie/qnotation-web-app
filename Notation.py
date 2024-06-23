from qiskit.quantum_info.operators import Operator
import numpy as np
import copy

class Notation:

    # Create list of grouped gates which can be used for circuit and Dirac display
    def create_circuit_dirac_gates_json(num_qubits, operation_list):
        circuit_json_list = []

        print("operation list in circuit", operation_list)

        circuit_json_list.append({"content": [[0] for i in range(0, num_qubits)], "type": "QUBIT","key": 0})

        for i in range(0, len(operation_list)):
            content = []
            for j in range(0, num_qubits):
                if j < len(operation_list[i]):
                    content.append({"gate": operation_list[i][j].operation.name})
                else:
                    content.append({"gate": "I"})

            circuit_json_list.append({"content": content, "type": "GATE","key": i+1})

        return circuit_json_list
    
    def simplify_values_matrix(matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                real_val = float(matrix[i][j].real)
                imag_val = float(matrix[i][j].imag)

                if real_val == 0.0 and imag_val == 0.0:
                    matrix[i][j] = 0.0
                elif imag_val == 0.0:
                    
                    matrix[i][j] = float(round(real_val,2))

        return matrix
    
    def simplify_values_state_vector(state_vector):
        for i in range(0, len(state_vector)):
            real_val = float(state_vector[i][0].real)
            imag_val = float(state_vector[i][0].imag)

            if real_val == 0.0 and imag_val == 0.0:
                state_vector[i][0] = 0.0
            elif imag_val == 0.0:
                
                state_vector[i][0] = float(round(real_val,2))

        return state_vector
    

    # Create list of state vectors for matrix display
    def create_matrix_state_vector_json(num_qubits, matrices=[]):

        matrix_vector_state_json = []

        vector = np.array([[1 if i == 0 else 0] for i in range(0, 2**num_qubits)])
        matrix_vector_state_json.append({"content": vector.tolist(), "type": "STATE","key": 0})

        for i in range(0, len(matrices)):
            vector = np.dot(matrices[i]["content"], vector)

            matrix_vector_state_json.append({"content": Notation.simplify_values_state_vector(vector.tolist()), "type": "GATE","key": i+1})

        return matrix_vector_state_json
    


    def get_list_of_qubit_indices_in_gate(gate):
        index_list = []
        for i in range(0, len(gate.qubits)):
            index_list.append(gate.qubits[i].index)

        print(index_list)
        return index_list
    
    # Create list of matrices of grouped gates which can be used matrix display
    def create_matrix_gate_json(num_qubits, operation_list):
        print("in function")


        identity_matrix = np.array([[1, 0], [0, 1]])

        matrix_gate_json_list = []

        # for each column...
        for i in range(0, len(operation_list)):

            gate_column = copy.deepcopy(operation_list[i])
            print("gate column", gate_column)
            matrix = []

            # Matrix calculations for column
            for j in range(0, num_qubits):

                print("looping through qubits")
                # try to find matrix in list of operations
                found = False
                k = 0
                while k < len(gate_column) and not found:

                    # if found, add matrix, remove from list
                    print("qubits", gate_column[k].qubits)
                    if j in Notation.get_list_of_qubit_indices_in_gate(gate_column[k]):
                        print("gate found for qubit")
                        if matrix == []:
                            matrix = Operator(gate_column[k].operation).data
                        else:
                            matrix = np.kron(matrix, Operator(gate_column[k].operation).data)
                        del gate_column[k]
                        found = True

                # if not found, add 2x2 identity matrix
                if not found:
                    if matrix == []:
                        matrix = identity_matrix
                    else:
                        matrix = np.kron(matrix, identity_matrix)

                    k =k+1

            matrix_gate_json_list.append({"content": Notation.simplify_values_matrix(matrix.tolist()), "type": "GATE","key": i+1})

        print("matrices", matrix_gate_json_list)

        return matrix_gate_json_list

    def create_matrix_gate_json_with_tensor_product(num_qubits, operation_list): 

        matrix_gate_json_list = []

        for i in range(0, len(operation_list)):

            matrices = []
            min_qubit = num_qubits
            max_qubit = 0

            for j in range(0, len(operation_list[i])):

                matrices.append(Notation.simplify_values_matrix(Operator(operation_list[i][0].operation).data))

            matrix_gate_json_list.append({"content": matrices, "type": "GATE","key": i+1})

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



