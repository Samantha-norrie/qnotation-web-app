from qiskit import *
from qiskit.quantum_info.operators import Operator
from qiskit.circuit import CircuitInstruction, Instruction, Qubit
from Errors import InvalidGate
import numpy as np
import copy

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
                case "cs":
                    qc.cs(gates[i].qubits[0].index, gates[i].qubits[1].index)
                case "cswap":
                    qc.cswap(gates[i].qubits[0].index, gates[i].qubits[1].index, gates[i].qubits[2].index)
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
    
    def get_gate_type(gate, gate_name, qubit):
        if gate_name in CONTROL_TARGET_GATE_NAMES:
            return CONTROL_GATE_TYPE if gate.qubits[0].index == qubit else TARGET_GATE_TYPE
        elif gate_name in CONTROL_CONTROL_TARGET_GATE_NAMES:
            return CONTROL_GATE_TYPE if gate.qubits[2].index != qubit else TARGET_GATE_TYPE
        elif gate_name in CONTROL_CONTROL_TARGET_GATE_NAMES:
            return CONTROL_GATE_TYPE if gate.qubits[3].index != qubit else TARGET_GATE_TYPE
        else:
            return NEUTRAL_GATE_TYPE  


    # TODO fix continuation flag
    # Create list of grouped gates which can be used for circuit and Dirac display
    def create_circuit_dirac_gates_json(num_qubits, grouped_gates):
        circuit_json_list = []

        circuit_json_list.append({"content": [[0] for i in range(0, num_qubits)], "type": "QUBIT","key": 0})

        for i in range(0, len(grouped_gates)):
            content = []
            for j in range(0, num_qubits):
                if type(grouped_gates[i][j]) == CircuitInstruction:
                    print("GATE", grouped_gates[i][j])
                    name = grouped_gates[i][j].operation.name
                    content.append({"gate": name.upper(), "gate_type": Notation.get_gate_type(grouped_gates[i][j], name, j), "continuation": False })
                elif grouped_gates[i][j] == "MARKED":
                    content.append({"gate": "", "gate_type": BETWEEN_GATE_TYPE, "continuation": True})
                else: 
                    content.append({"gate": "I", "gate_type": NEUTRAL_GATE_TYPE, "continuation": False})
        

    
            circuit_json_list.append({"content": content, "type": "GATE","key": i+1})

        return circuit_json_list

    def simplify_single_matrix(matrix):

        for j in range(0, len(matrix)):
            for k in range(0, len(matrix[j])):

                real_val = float(matrix[j][k].real)
                imag_val = float(matrix[j][k].imag)

                if real_val == 0.0 and imag_val == 0.0:
                    matrix[j][k] = 0.0
                elif round(imag_val,4) == 0.0:     
                    matrix[j][k] = float(round(real_val,2))
                elif round(imag_val,4) == 1.0:
                    matrix[j][k] = "i"
                else:
                    matrix[j][k] = str(round(real_val,2)) + str(round(imag_val,2)) + "i"
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
 
    def create_tensor_product_matrix_gate_json(num_qubits, grouped_gates):
        identity_matrix = np.array([[1, 0], [0, 1]])

        matrix_gate_json_list = []

        # for each column...
        for i in range(0, len(grouped_gates)):

            matrices = []
            # Matrix calculations for column
            for j in range(0, num_qubits):
                if grouped_gates[i][j] == "MARKED":
                    continue
                elif grouped_gates[i][j] == None:
                    matrices.append(identity_matrix.tolist())
                else:
                    matrices.append(Notation.simplify_single_matrix(Operator(grouped_gates[i][j].operation).data.tolist()).copy())

            matrix_gate_json_list.append({"content": matrices, "type": "GATE","key": i+1})

        return matrix_gate_json_list


    # Create list of matrices of grouped gates which can be used matrix display
    def create_matrix_gate_json(num_qubits, grouped_gates, little_endian):

        identity_matrix = np.array([[1, 0], [0, 1]])

        matrix_gate_json_list = []

        # for each column...
        for i in range(0, len(grouped_gates)):

            matrix = []

            # current_col = grouped_gates[i].deepcopy()
            # if little_endian:
            #     current_col = vurr
            # Matrix calculations for column
            for j in range(0, num_qubits):
                if grouped_gates[i][j] == "MARKED":
                    continue
                elif matrix == [] and grouped_gates[i][j] == None:
                    matrix = identity_matrix
                elif matrix == []:
                    matrix = Operator(grouped_gates[i][j].operation).data
                elif grouped_gates[i][j] == None:
                    matrix = np.kron(matrix, identity_matrix)
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

    #TODO optimize more
    def group_gates(num_qubits, circuit, little_endian=True):
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

        return columns



