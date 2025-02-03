from qiskit import *
from qiskit.quantum_info.operators import Operator
from qiskit.circuit import CircuitInstruction
import numpy as np
from utils import * 

# MATRIX

def simplify_single_matrix(matrix):
    """
    Simplifies matrix TODO: improve simplification logic

    Args:
        matrix (list[complex]): a list of matrices representing the columns in the quantum circuit

    Returns:
        list[object]: Simplified matrix
    """
    
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
    
def simplify_matrices_json(matrices):
    """
    Wrapper for simplifying list of JSON objects describing matrices used in equation portion of matrix notation component

    Args:
        matrices (list[object]): a list of matrices representing the columns in the quantum circuit

    Returns:
        list[object]: list of JSON objects with simplified matrices
    """
    for i in range(0, len(matrices)):
        matrix =  matrices[i]["content"]
        matrix = simplify_single_matrix(matrix)
    return matrices

def create_matrix_state_vector_json(num_qubits, matrices):
    """
    Creates JSON objects of state vectors representing the state of the quantum circuit at each of its columns

    Args:
        num_qubits (int): the number of qubits in the quantum circuit
        matrices (list[object]): a list of matrices representing the columns in the quantum circuit

    Returns:
        list[object]: list of state vector JSON objects
    """

    matrix_vector_state_json = []

    # Initial state (no gates applied yet) representing all qubits being set to 0
    vector = np.array([[1 if i == 0 else 0] for i in range(0, 2**num_qubits)])

    matrix_vector_state_json.append({"content": vector.tolist(), "type": STATE,"key": 0})

    for i in range(0, len(matrices)):

        vector = np.dot(matrices[i]["content"], vector)
        matrix_vector_state_json.append({"content": simplify_values_state_vector(vector.tolist()), "type": GATE,"key": i+1})

    return matrix_vector_state_json

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

def create_tensor_product_matrix_gate_json(num_qubits, grouped_gates, little_endian=False):
    """
    Creates lists of matrices for tensor product setting

    Args:
        num_qubits (int): number of qubits in the circuit
        grouped_gates (list[object]): quantum circuit being operated on
        little_endian (boolean): flag for endianess

    Returns:
        list[object]: list of JSON objects describing matrices for tensor product setting
    """

    matrix_gate_json_list = []

    # Go through each grouped gate column and check each qubit
    for i in range(0, len(grouped_gates)):

        matrices = []
        current_qubit_in_column = grouped_gates[i][j]

        # Matrix calculations for column
        for j in range(0, num_qubits):

            # format and append matrices found to list
            if type(current_qubit_in_column) == CircuitInstruction:
                if is_non_neighbouring_gate(current_qubit_in_column):
                    if little_endian:
                        matrices.append(simplify_single_matrix(Operator(get_non_neighbouring_matrix_little_endian(current_qubit_in_column)).data.tolist()).copy())
                    else:
                        matrices.append(simplify_single_matrix(Operator(get_matrix_for_multi_qubit_big_endian(grouped_gates[i][j])).data.tolist()).copy())
                else:
                    matrices.append(simplify_single_matrix(Operator(current_qubit_in_column.operation).data.tolist()).copy())

            # append identity matrix if qubit is not being used by any other gate
            elif current_qubit_in_column == NOT_INVOLVED:
                matrices.append(IDENTITY_MATRIX.tolist())
                
        matrix_gate_json_list.append({"content": matrices, "type": GATE,"key": i+1})
    return matrix_gate_json_list

def create_matrix_gate_json(num_qubits, grouped_gates, little_endian=False):
    """
    Creates list of JSON objects which contain matrix representations of gate columns, their types (GATE), and their indices

    Args:
        num_qubits (int): the number of qubits in the circuit
        grouped_gates (list[object]): the quantum circuit being operated on

    Returns:
        list[object]: A list of JSON objects representing the given grouped gates in matrix form
    """

    matrix_gate_json_list = []

    # Go through each grouped gate column and check each qubit
    for i in range(0, len(grouped_gates)):

        # Store computed matrix for column in matrix variable
        matrix = []

        for j in range(0, num_qubits):

            current_qubit_in_column = grouped_gates[i][j]

            # Continue if current qubit does not contain a CircuitInstruction
            if current_qubit_in_column == AUXILIARY or current_qubit_in_column == CONTROL or current_qubit_in_column == TARGET:
                continue

            # Set matrix to equal identity matrix if no gate has been applied yet and qubit is not involved in any gate
            elif len(matrix) == 0 and current_qubit_in_column == NOT_INVOLVED:
                matrix = IDENTITY_MATRIX

            # Apply identity matrix to existing matrix if qubit is not involved in any gate
            elif current_qubit_in_column == NOT_INVOLVED:
                matrix = np.kron(matrix, IDENTITY_MATRIX)

            # If no matrix has been applied yet..
            elif len(matrix) == 0:

                # little endian
                if little_endian:
                    matrix = get_non_neighbouring_matrix_little_endian(current_qubit_in_column) if is_non_neighbouring_gate(current_qubit_in_column) else Operator(current_qubit_in_column.operation).data

                # big endian
                else:
                    if len(current_qubit_in_column.qubits) == 1:
                        matrix = Operator(current_qubit_in_column.operation).data
                    else:
                        matrix = get_matrix_for_multi_qubit_big_endian(current_qubit_in_column)

            # If matrices have already been applied...     
            else:

                # little endian
                if little_endian:
                    matrix = np.kron(matrix, get_non_neighbouring_matrix_little_endian(current_qubit_in_column) if is_non_neighbouring_gate(current_qubit_in_column) else Operator(current_qubit_in_column.operation).data)
                
                # big endian
                else:
                    if len(current_qubit_in_column.qubits) == 1:
                        matrix = np.kron(matrix, Operator(current_qubit_in_column.operation).data)
                    else:
                        matrix = np.kron(matrix, get_matrix_for_multi_qubit_big_endian(current_qubit_in_column))
        
        matrix_gate_json_list.append({"content": matrix.tolist(), "type": GATE,"key": i+1})

    return matrix_gate_json_list
# CIRCUIT AND DIRAC
def create_circuit_dirac_gates_json(num_qubits, grouped_gates):
    """
    Creats JSON objects for describing data for equation components for circuit and Dirac

    Args:
        num_qubits (int): the number of qubits in the quantum circuit
        grouped_gates (list[object]): the quantum circuit being operated on

    Returns:
        list[object]: list of JSON objects containing information for circuit and Dirac equation components
    """
    circuit_dirac_gate_json_list = []

    circuit_dirac_gate_json_list.append({"content": [[0] for i in range(0, num_qubits)], "type": STATE, "key": 0})

    # Go through each grouped gate column and check each qubit
    for i in range(0, len(grouped_gates)):

        content = []

        for j in range(0, num_qubits):
            current_qubit_in_column = grouped_gates[i][j]

            if type(current_qubit_in_column) == CircuitInstruction:
                content.append({"gate": current_qubit_in_column.operation.name.upper(), "gate_type": GATE_INFO})
            elif current_qubit_in_column == NOT_INVOLVED:
                content.append({"gate": IDENTITY_MATRIX_NAME, "gate_type": current_qubit_in_column})
            else: 
                content.append({"gate": "", "gate_type": current_qubit_in_column})

        circuit_dirac_gate_json_list.append({"content": content, "type": GATE, "key": i+1})

    return circuit_dirac_gate_json_list

def format_matrix_state_vectors_for_dirac_state_json(num_qubits, state_vector):
    """
    Make Dirac states using matrix state vectors. Only make states that have an amplitude != 0

    Args:
        num_qubits (int): number of qubits in the circuit
        state_vector (list[object]): list of JSON objects describing state vectors

    Returns:
        list[object]: A list of JSON objects representing the given state vectors as Dirac states
    """

    dirac_state_json = []
    format_val = '0' + str(num_qubits)+'b'

    for i in range(0, len(state_vector)):
        values = []
        for j in range(0, len(state_vector[i]["content"])):

            # if the state exists, convert it into binary
            if state_vector[i]["content"][j][0] != 0:
                values.append({"bin": format(j, format_val), "scalar": state_vector[i]["content"][j][0]})
        dirac_state_json.append({"content": values, "type": STATE, "key": i})

    return dirac_state_json