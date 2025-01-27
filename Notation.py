from qiskit import *
from qiskit.quantum_info.operators import Operator
from qiskit.circuit import CircuitInstruction, Instruction, Qubit
from errors import InvalidGateError, InputError
import numpy as np
import math
import subprocess
import sys
import os
import tempfile
from utils import * 

class notation:
    
    def get_matrix_for_multi_qubit_big_endian(gate):
        name = gate.operation.name
        non_neighbouring = notation.is_non_neighbouring_gate(gate)
        match name:
            case "ch":
                return CH_BE
            case "cp":
                if non_neighbouring:
                    phi = gate.operation.params[0]
                    if non_neighbouring:
                        return get_cp(phi, 1)
                    return get_cp()
                return Operator(gate.operation).data 
            case "crx":
                theta = gate.operation.params[0]
                if non_neighbouring:
                    return get_crx(theta, False, 1)
                return get_crx(theta)
            case "cry":
                theta = gate.operation.params[0]
                if non_neighbouring:
                    return get_cry(theta,1)
                return get_cry(theta)
            case "crz":
                theta = gate.operation.params[0]
                if non_neighbouring:
                    return get_crz(theta, 1)
                return get_crz(theta)
            case "cs":
                return Operator(gate.operation).data
            case "csx":
                return CSX_BE
            case "cswap":
                return CSWAP_BE
            case "cx":
                if non_neighbouring:
                    return CX_BE_ONE_GAP
                return CX_BE
            case "cy":
                if non_neighbouring:
                    return CY_BE_ONE_GAP
                return CY_BE
            case "cz":
                return Operator(gate.operation).data 
            case _:
                return []
    
    # Create list of grouped gates which can be used for circuit and Dirac display
    def create_circuit_dirac_gates_json(num_qubits, grouped_gates):
        circuit_json_list = []

        circuit_json_list.append({"content": [[0] for i in range(0, num_qubits)], "type": "QUBIT","key": 0})

        incomplete_gate = False
        for i in range(0, len(grouped_gates)):
            content = []
            for j in range(0, num_qubits):
                if type(grouped_gates[i][j]) == CircuitInstruction:

                    name = grouped_gates[i][j].operation.name

                    if len(grouped_gates[i][j].qubits) > 1:
                        incomplete_gate = not incomplete_gate
                        content.append({"gate": name.upper(), "gate_type": CONTROL_GATE_TYPE})
                    else:
                        content.append({"gate": name.upper(), "gate_type": NEUTRAL_GATE_TYPE})
                elif grouped_gates[i][j] == "MARKED":
                    incomplete_gate = not incomplete_gate
                    content.append({"gate": "" , "gate_type": TARGET_GATE_TYPE})
                else: 
                    if incomplete_gate:
                        content.append({"gate": "", "gate_type": BETWEEN_GATE_TYPE})
                    else:
                        content.append({"gate": "I", "gate_type": NEUTRAL_GATE_TYPE})
        

    
            circuit_json_list.append({"content": content, "type": "GATE","key": i+1})

        return circuit_json_list

    def simplify_single_matrix(matrix):
        
        for j in range(0, len(matrix)):
            for k in range(0, len(matrix[j])):

                real_val = float(matrix[j][k].real)
                imag_val = float(matrix[j][k].imag)

                if real_val == 0.0 and imag_val == 0.0:
                    matrix[j][k] = 0.00
                elif round(imag_val,4) == 0.0:     
                    matrix[j][k] = float("{:.2f}".format(real_val))
                elif round(imag_val,4) == 1.0:
                    matrix[j][k] = " i "
                else:
                    matrix[j][k] = "{:.2f}".format(real_val + imag_val) + "i"
        return matrix
       
    def simplify_values_matrix(matrices):
        for i in range(0, len(matrices)):
            matrices[i]["content"] = notation.simplify_single_matrix(matrices[i]["content"])
        return matrices
    
    def simplify_values_state_vector(state_vector):

        for i in range(0, len(state_vector)):
            real_val = float(state_vector[i][0].real)
            imag_val = float(state_vector[i][0].imag)

            if real_val == 0.0 and imag_val == 0.0:
                state_vector[i][0] = 0.0
            elif round(imag_val, 4) == 0.0:
                
                state_vector[i][0] = float(round(real_val,2))
            elif round(imag_val,4) == 1.0:
                state_vector[i][0] = "i"
            else:
                state_vector[i][0] = str(round(real_val,2)) + str(round(imag_val,2)) + "i"

        return state_vector
    

    # Create list of state vectors for matrix display
    def create_matrix_state_vector_json(num_qubits, matrices=[]):

        matrix_vector_state_json = []
        vector = np.array([[1 if i == 0 else 0] for i in range(0, 2**num_qubits)])

        matrix_vector_state_json.append({"content": vector.tolist(), "type": "STATE","key": 0})

        for i in range(0, len(matrices)):

            vector = np.dot(matrices[i]["content"], vector)
            matrix_vector_state_json.append({"content": notation.simplify_values_state_vector(vector.tolist()), "type": "GATE","key": i+1})

        return matrix_vector_state_json
    
    def get_list_of_qubit_indices_in_gate(gate):
        index_list = []
        for i in range(0, len(gate.qubits)):
            index_list.append(gate.qubits[i].index)

        return index_list
 
    def create_tensor_product_matrix_gate_json(num_qubits, grouped_gates, little_endian=False):
        identity_matrix = np.array([[1, 0], [0, 1]])

        matrix_gate_json_list = []

        # for each column...
        for i in range(0, len(grouped_gates)):

            matrices = []
            incomplete_gate = False
            # Matrix calculations for column
            for j in range(0, num_qubits):
                if len(grouped_gates[i][j]) == 0 and not incomplete_gate:
                    matrices.append(identity_matrix.tolist())
                elif len(grouped_gates[i][j]) == 0:
                    continue
                elif grouped_gates[i][j] == "MARKED":
                    incomplete_gate = not incomplete_gate
                    continue
                else:
                    if len(grouped_gates[i][j].qubits) > 1 and not little_endian:
                        incomplete_gate = not incomplete_gate
                        if notation.is_non_neighbouring_gate(grouped_gates[i][j]) and little_endian:
                            matrices.append(notation.simplify_single_matrix(Operator(get_non_neighbouring_LE_matrix(grouped_gates[i][j])).data.tolist()).copy())
                        elif not little_endian:
                            matrices.append(notation.simplify_single_matrix(Operator(notation.get_matrix_for_multi_qubit_big_endian(grouped_gates[i][j])).data.tolist()).copy())
                    else:
                        matrices.append(notation.simplify_single_matrix(Operator(grouped_gates[i][j].operation).data.tolist()).copy())

            matrix_gate_json_list.append({"content": matrices, "type": "GATE","key": i+1})
        return matrix_gate_json_list

    # TODO implement for gates that involve more than 2 qubits
    def is_non_neighbouring_gate(gate):
        num_qubits = len(gate.qubits)
        if num_qubits > 1:
            if math.fabs(gate.qubits[0].index-gate.qubits[1].index) > 1:
                return True
            
        return False


    # Create list of matrices of grouped gates which can be used matrix display
    #TODO clean
    # TODO implement non neighbouring gate flag
    def create_matrix_gate_json(num_qubits, grouped_gates, little_endian=False):

        identity_matrix = np.array([[1, 0], [0, 1]])

        matrix_gate_json_list = []

        # for each column...
        for i in range(0, len(grouped_gates)):

            matrix = []

            # Matrix calculations for column
            gate_incomplete = False
            for j in range(0, num_qubits):
                # print("m", matrix)
                # if qubit is a target qubit, end 
                if grouped_gates[i][j] == "MARKED":
                    gate_incomplete = not gate_incomplete
                    continue
                elif gate_incomplete and len(grouped_gates[i][j]) == 0:
                    continue

                # if there is no gate in the progress of being described, apply an identity matrix 
                elif not gate_incomplete and len(matrix) == 0 and len(grouped_gates[i][j]) == 0:
                    matrix = identity_matrix

                # if a matrix has been applied already but there is no gate at qubit or gate in progress, apply identity   
                elif not gate_incomplete and len(grouped_gates[i][j]) == 0:
                    matrix = np.kron(matrix, identity_matrix)

                # if no matrix has been applied yet...
                elif len(matrix) == 0:
                    if gate_incomplete:
                        gate_incomplete = False
                    elif notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                        gate_incomplete = True

                    # if little endian, apply as normal
                    if little_endian:

                        # if single qubit gate, apply as normal
                        matrix = get_non_neighbouring_LE_matrix(grouped_gates[i][j]) if notation.is_non_neighbouring_gate(grouped_gates[i][j]) else Operator(grouped_gates[i][j].operation).data

                    # if big endian, ensure that the correct matrix is being applied (for multi-qubit gates only)
                    else:
                        new_matrix = notation.get_matrix_for_multi_qubit_big_endian(grouped_gates[i][j])

                        if len(new_matrix) != 0:
                            if notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                                gate_incomplete = not gate_incomplete

                            matrix = new_matrix
                            gate_incomplete = not gate_incomplete
                        
                        else:
                            matrix = Operator(grouped_gates[i][j].operation).data
                elif little_endian:
                    matrix = np.kron(matrix, get_non_neighbouring_LE_matrix(grouped_gates[i][j]) if notation.is_non_neighbouring_gate(grouped_gates[i][j]) else Operator(grouped_gates[i][j].operation).data)
                else:
                    if gate_incomplete:
                        gate_incomplete = False
                    elif notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                        gate_incomplete = True
                    if little_endian:
                        matrix = np.kron(matrix, get_non_neighbouring_LE_matrix(grouped_gates[i][j]) if notation.is_non_neighbouring_gate(grouped_gates[i][j]) else Operator(grouped_gates[i][j].operation).data)
                    else:
                        new_matrix = notation.get_matrix_for_multi_qubit_big_endian(grouped_gates[i][j])

                        if new_matrix != []:
                            if notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                                gate_incomplete = not gate_incomplete

                            matrix = np.kron(matrix, new_matrix)
                        else:
                            matrix = np.kron(matrix, Operator(grouped_gates[i][j].operation).data)
            
            matrix_gate_json_list.append({"content": matrix.tolist(), "type": "GATE","key": i+1})

        return matrix_gate_json_list

    def format_matrix_state_vectors_for_dirac_state(num_qubits, state_vector):

        dirac_state_json = []
        format_val = '0' + str(num_qubits)+'b'

        for i in range(0, len(state_vector)):
            values = []
            for j in range(0, len(state_vector[i]["content"])):

                # if the state exists, convert it into binary
                if state_vector[i]["content"][j][0] != 0:
                    values.append({"bin": format(j, format_val), "scalar": state_vector[i]["content"][j][0]})
            dirac_state_json.append({"content": values, "type": "STATE", "key": i})

        return dirac_state_json