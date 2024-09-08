from qiskit import *
from qiskit.quantum_info.operators import Operator
from qiskit.circuit import CircuitInstruction, Instruction, Qubit
from Errors import InvalidGate
import numpy as np
import copy
import math
import subprocess
import sys
import os
import tempfile
from Utils import * 

class Notation:

    #  Process circuit received from frontend
    def process_circuit_received(qc_string):
        qc_code_list = qc_string.split('\n')

        qc_string_formatted = ""

        end_of_imports_found = False
        for i in range(0, len(qc_code_list)):
            if not end_of_imports_found and "import numpy as np" in qc_code_list[i]:
                qc_string_formatted = qc_string_formatted + qc_code_list[i] + "\ndef main():\n"
                end_of_imports_found = True
            elif end_of_imports_found:
                qc_string_formatted = qc_string_formatted + "   " + qc_code_list[i]  + "\n"
            else:
                qc_string_formatted = qc_string_formatted + qc_code_list[i] + "\n"
        qc_string_formatted = qc_string_formatted + "   " + "print([qc.num_qubits, qc.data])" + "\nmain()"

        circuit_details = []

        # Use a temporary file to execute the code securely
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
            temp_file.write(qc_string_formatted.encode('utf-8'))
            temp_file_name = temp_file.name
        try:
            # Execute the code in the temporary file using a subprocess
            result = subprocess.run([sys.executable, temp_file_name], capture_output=True, text=True, timeout=5)

            output = result.stdout

            circuit_details = eval(output)
            error = result.stderr
        except subprocess.TimeoutExpired:
            output = ""
            error = "Execution timed out"
            print("ERROR", error)
        except Exception as e:
            output = ""
            error = str(e)
            print("ERROR1", error)
        finally:
            # Ensure the temporary file is deleted after execution
            os.remove(temp_file_name)

        return circuit_details
    
    #TODO fix eventually
    def convert_input_gates(num_qubits, gates):

        qc = QuantumCircuit(num_qubits)
        for i in range(0, len(gates)):
            match gates[i].operation.name:
                case "cp":
                    qc.cp(gates[i].operation.params[0], gates[i].qubits[0].index, gates[i].qubits[1].index)       
                case "cs":
                    qc.cs(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "cswap":
                    qc.cswap(gates[i].qubits[0].index, gates[i].qubits[1].index, gates[i].qubits[2].index)
                case "crx":
                    qc.crx(gates[i].operation.params[0], gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "csx":
                    qc.csx(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "cx":
                    qc.cx(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "cy":
                    qc.cy(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "cz":
                    qc.cz(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "dcx":
                    qc.dcx(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "h":
                    qc.h(gates[i].qubits[0].index)
                case "iswap":
                    qc.iswap(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "p":
                    qc.p(gates[i].operation.params[0], gates[i].qubits[0].index)
                case "r":
                    qc.r(gates[i].operation.params[0], gates[i].operation.params[1], gates[i].qubits[0].index)
                case "rcccx":
                    qc.rcccx(gates[i].qubits[0].index, gates[i].qubits[1].index, gates[i].qubits[2].index, gates[i].qubits[3].index)
                case "rccx":
                    qc.rccx(gates[i].qubits[0].index, gates[i].qubits[1].index, gates[i].qubits[2].index)
                case "rv":
                    qc.rv(gates[i].operation.params[0], gates[i].operation.params[1], gates[i].operation.params[0], gates[i].qubits[0].index)
                case "rx":
                    qc.rx(gates[i].operation.params[0], gates[i].qubits[0].index)
                case "rxx":
                    qc.rxx(gates[i].operation.params[0], gates[i].qubits[0].index, gates[i].qubits[1].index)  
                case "ry":
                    qc.ry(gates[i].operation.params[0], gates[i].qubits[0].index)   
                case "ryy":
                    qc.ryy(gates[i].operation.params[0], gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "rz":
                    qc.rz(gates[i].operation.params[0], gates[i].qubits[0].index)
                case "rzx":
                    qc.rzx(gates[i].operation.params[0], gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "rzz":
                    qc.rzz(gates[i].operation.params[0], gates[i].qubits[0].index, gates[i].qubits[1].index) 
                case "s":
                    qc.s(gates[i].qubits[0].index)
                case "sdg":
                    qc.sdg(gates[i].qubits[0].index)
                case "swap":
                    qc.swap(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "sx":
                    qc.sx(gates[i].qubits[0].index)     
                case "sxdg":
                    qc.sxdg(gates[i].qubits[0].index)
                case "t":
                    qc.t(gates[i].qubits[0].index) 
                case "tdg":
                    qc.tdg(gates[i].qubits[0].index)
                case "u":
                    qc.u(gates[i].operation.params[0], gates[i].operation.params[1], gates[i].operation.params[2], gates[i].qubits[0].index)                     
                case "x":
                    qc.x(gates[i].qubits[0].index)
                case "y":
                    qc.y(gates[i].qubits[0].index)
                case "z":
                    qc.z(gates[i].qubits[0].index)
                case _:
                    raise InvalidGate
                
        return qc
    
    def get_matrix_for_multi_qubit_big_endian(gate):
        name = gate.operation.name
        non_neighbouring = Notation.is_non_neighbouring_gate(gate)
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
                # same lol
                return Operator(gate.operation).data 
            case _:
                return []
    
    # TODO fix continuation flag
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
                    matrix[j][k] = 0.000
                elif round(imag_val,4) == 0.0:     
                    matrix[j][k] = float("{:.3f}".format(real_val))
                elif round(imag_val,4) == 1.0:
                    matrix[j][k] = " i "
                else:
                    matrix[j][k] = "{:.3f}".format(real_val + imag_val) + "i"
        return matrix
       
    def simplify_values_matrix(matrices):
        for i in range(0, len(matrices)):
            matrices[i]["content"] = Notation.simplify_single_matrix(matrices[i]["content"])
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
            matrix_vector_state_json.append({"content": Notation.simplify_values_state_vector(vector.tolist()), "type": "GATE","key": i+1})

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
                if grouped_gates[i][j] == None and not incomplete_gate:
                    matrices.append(identity_matrix.tolist())
                elif grouped_gates[i][j] == None:
                    continue
                elif grouped_gates[i][j] == "MARKED":
                    incomplete_gate = not incomplete_gate
                    continue
                else:
                    if len(grouped_gates[i][j].qubits) > 1:
                        incomplete_gate = not incomplete_gate
                        if Notation.is_non_neighbouring_gate(grouped_gates[i][j]) and little_endian:
                            matrices.append(Notation.simplify_single_matrix(Operator(get_non_neighbouring_LE_matrix(grouped_gates[i][j])).data.tolist()).copy())
                    else:
                        matrices.append(Notation.simplify_single_matrix(Operator(grouped_gates[i][j].operation).data.tolist()).copy())

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
            print("INITIAL GATES", grouped_gates)

            # Matrix calculations for column
            gate_incomplete = False
            for j in range(0, num_qubits):
                # if qubit is a target qubit, end 
                if grouped_gates[i][j] == "MARKED":
                    gate_incomplete = not gate_incomplete
                    continue
                elif gate_incomplete and grouped_gates[i][j] == None:
                    continue
                # if there is no gate in the progress of being described, apply an identity matrix 
                elif not gate_incomplete and matrix == [] and grouped_gates[i][j] == None:
                    matrix = identity_matrix
                    print("FIRST IDENTITY")
                # if a matrix has been applied already but there is no gate at qubit or gate in progress, apply identity   
                elif not gate_incomplete and grouped_gates[i][j] == None:
                    matrix = np.kron(matrix, identity_matrix)
                    print("SECOND IDENTITY")
                # if no matrix has been applied yet...
                elif matrix == []:
                    if gate_incomplete:
                        gate_incomplete = False
                    elif Notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                        gate_incomplete = True
                    # if little endian, apply as normal
                    if little_endian:
                        # if single qubit gate, apply as normal
                        # TODO is distinction between single and multi needed for little endian?
                        matrix = get_non_neighbouring_LE_matrix(grouped_gates[i][j]) if Notation.is_non_neighbouring_gate(grouped_gates[i][j]) else Operator(grouped_gates[i][j].operation).data
                    # if big endian, ensure that the correct matrix is being applied (for multi-qubit gates only)
                    else:
                        new_matrix = Notation.get_matrix_for_multi_qubit_big_endian(grouped_gates[i][j])
                        print("new matrix", new_matrix)
                        if new_matrix != []:
                            print("applying!")
                            if Notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                                gate_incomplete = not gate_incomplete

                            matrix = new_matrix
                            gate_incomplete = not gate_incomplete
                            print("after application", matrix)
                        
                        else:
                            matrix = Operator(grouped_gates[i][j].operation).data
                elif little_endian:
                    print("IN LITTLE ENDIAN")
                    matrix = np.kron(matrix, get_non_neighbouring_LE_matrix(grouped_gates[i][j]) if Notation.is_non_neighbouring_gate(grouped_gates[i][j]) else Operator(grouped_gates[i][j].operation).data)
                else:
                    if gate_incomplete:
                        gate_incomplete = False
                    elif Notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                        gate_incomplete = True
                    if little_endian:
                        print("IN LITTLE ENDIAN")
                        matrix = np.kron(matrix, get_non_neighbouring_LE_matrix(grouped_gates[i][j]) if Notation.is_non_neighbouring_gate(grouped_gates[i][j]) else Operator(grouped_gates[i][j].operation).data)
                    else:
                        new_matrix = Notation.get_matrix_for_multi_qubit_big_endian(grouped_gates[i][j])
                        print("new matrix", new_matrix)
                        if new_matrix != []:
                            print("applying!")
                            if Notation.is_non_neighbouring_gate(grouped_gates[i][j]):
                                gate_incomplete = not gate_incomplete

                            matrix = np.kron(matrix, new_matrix)
                            print("after application", matrix)
                        else:
                            matrix = np.kron(matrix, Operator(grouped_gates[i][j].operation).data)
            
            matrix_gate_json_list.append({"content": matrix.tolist(), "type": "GATE","key": i+1})
        print("finished matrix building")
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
    
    #TODO optimize more
    def group_gates(num_qubits, circuit, little_endian=False):
        gates = circuit.data

        columns = [[None for i in range(0, num_qubits)]]
        column_pointer = 0

        while len(gates) > 0:
            gate = gates.pop(0)
            gate_indices = Notation.get_list_of_qubit_indices_in_gate(gate)
            available = True
            for i in range(0, len(gate_indices)):
                if columns[column_pointer][gate_indices[i]] != None:
                    available = False
            if not available:
                column_pointer = column_pointer + 1
                if column_pointer >= len(columns):
                    columns.append([None for j in range(0, num_qubits)])
            for i in range(0, len(gate_indices)):
                if i == 0:
                    columns[column_pointer][gate_indices[i]] = gate
                else:
                    # print("MARKED A STATE")
                    columns[column_pointer][gate_indices[i]] = "MARKED"

        if little_endian:
            for i in range(0, len(columns)):
                columns[i].reverse()
        # else:
        #     Notation.fix_multi_qubit_gates_for_big_endian(columns)

        return columns