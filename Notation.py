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

class Notation:

    #  Process circuit received from frontend
    def process_circuit_received(qc_string):
        qc_code_list = qc_string.split('\n')
        print(qc_string)

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
    
    def convert_input_gates(num_qubits, gates):
        print(gates)
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
                # case "r":
                #     qc.r(gates[i].operation.params[0], gates[i].operation.params[1], gates[i].qubits[0].index)
                # case "rcccx":
                #     qc.rcccx(gates[i].qubits[0].index, gates[i].qubits[1].index, gates[i].qubits[2].index, gates[i].qubits[3].index)
                # case "rccx":
                #     qc.rccx(gates[i].qubits[0].index, gates[i].qubits[1].index, gates[i].qubits[2].index)
                case "x":
                    qc.x(gates[i].qubits[0].index)
                case "y":
                    qc.y(gates[i].qubits[0].index)
                case "z":
                    qc.z(gates[i].qubits[0].index)
                case _:
                    raise InvalidGate
                
        return qc

    # Create list of grouped gates which can be used for circuit and Dirac display
    def create_circuit_dirac_gates_json(num_qubits, operation_list):
        circuit_json_list = []

        circuit_json_list.append({"content": [[0] for i in range(0, num_qubits)], "type": "QUBIT","key": 0})

        for i in range(0, len(operation_list)):
            content = []
            multi_qubits = []
            for j in range(0, num_qubits):
                if j < len(operation_list[i]):
                    content.append({"gate": operation_list[i][j].operation.name, "continuation": False })
                    if len(operation_list[i][j].qubits) > 1:
                        for k in range(0, len(operation_list[i][j].qubits)):
                            multi_qubits.append({"qubit": operation_list[i][j].qubits[k].index, "gate": operation_list[i][j].operation.name})
                else:
                    found = False
                    for k in range(0, len(multi_qubits)):
                        if not found and j == multi_qubits[k]["qubit"]:
                            content.append({"gate": multi_qubits[k]["gate"], "continuation": True})
                            found = True
                    if not found:
                        content.append({"gate": "I", "continuation": False})

            circuit_json_list.append({"content": content, "type": "GATE","key": i+1})

        return circuit_json_list
    
    def simplify_values_matrix(matrices):
        for i in range(0, len(matrices)):
            matrix = matrices[i]["content"]
            for j in range(0, len(matrix)):
                for k in range(0, len(matrix[j])):
                    real_val = float(matrix[j][k].real)
                    imag_val = float(matrix[j][k].imag)
                    print("real val", real_val, "imag val", imag_val)

                    if real_val == 0.0 and imag_val == 0.0:
                        matrix[j][k] = 0.0
                    elif round(imag_val,4) == 0.0:     
                        matrix[j][k] = float(round(real_val,2))
                    elif round(imag_val,4) == 1.0:
                        matrix[j][k] = "i"
                    else:
                    # elif round(real_val,4) != 0.0 and round(imag_val,4) != 0.0: 
                        matrix[i][j] = str(round(real_val,2)) + str(round(imag_val,2)) + "i"

        return matrices
    
    def simplify_values_state_vector(state_vector):
        print("state vector before simplification", state_vector)
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
        print("in create_matrix_state_vector_json")
        matrix_vector_state_json = []
        vector = np.array([[1 if i == 0 else 0] for i in range(0, 2**num_qubits)])
        # vector = np.array([[np.complex128(1+0j) if i == 0 else np.complex128(0+0j)] for i in range(0, 2**num_qubits)])
        matrix_vector_state_json.append({"content": vector.tolist(), "type": "STATE","key": 0})
        print("first vector added")
        for i in range(0, len(matrices)):
            print("types", type(vector), type(matrices[i]["content"]))
            print("VECTOR", vector)
            print("CONTENT", matrices[i]["content"])
            vector = np.dot(matrices[i]["content"], vector)
            print("afer dot")

            matrix_vector_state_json.append({"content": Notation.simplify_values_state_vector(vector.tolist()), "type": "GATE","key": i+1})
        print("at return")
        return matrix_vector_state_json
    


    def get_list_of_qubit_indices_in_gate(gate):
        index_list = []
        for i in range(0, len(gate.qubits)):
            index_list.append(gate.qubits[i].index)

        return index_list
    
    # Create list of matrices of grouped gates which can be used matrix display
    def create_matrix_gate_json(num_qubits, operation_list):

        identity_matrix = np.array([[1, 0], [0, 1]])

        matrix_gate_json_list = []

        # for each column...
        for i in range(0, len(operation_list)):
            print("column", i)

            gate_column = copy.deepcopy(operation_list[i])
            matrix = []

            accounted_for_qubits = []
            # Matrix calculations for column
            for j in range(0, num_qubits):

                # try to find matrix in list of operations
                found = False
                k = 0
                while k < num_qubits and not found:
                    print("WHILE LOOP", num_qubits, k)

                    # if found, add matrix, remove from list
                    if k in Notation.get_list_of_qubit_indices_in_gate(gate_column[k]) and k not in accounted_for_qubits:
                        for l in range(0, len(gate_column[k].qubits)):
                            if not gate_column[k].qubits[l].index in accounted_for_qubits:
                                accounted_for_qubits.append(gate_column[k].qubits[l].index)

                        print("ACCOUNTED FOR QUBITS", accounted_for_qubits)
                        if matrix == []:
                            print("in problematic part",gate_column[k].operation)
                            matrix = Operator(gate_column[k].operation).data
                        else:
                            matrix = np.kron(matrix, Operator(gate_column[k].operation).data)
                        # del gate_column[k]
                        found = True
                    k = k+1

                # if not found, add 2x2 identity matrix
                if not found and j not in accounted_for_qubits:
                    print("in identity add")
                    if matrix == []:
                        matrix = identity_matrix
                    else:
                        matrix = np.kron(matrix, identity_matrix)

                    # k = k+1
            


            matrix_gate_json_list.append({"content": matrix.tolist(), "type": "GATE","key": i+1})
        print("returning")
        return matrix_gate_json_list

    def format_matrix_state_vectors_for_dirac_state(state_vector):
        # print("state vector list", state_vector)
        dirac_state_json = []

        for i in range(0, len(state_vector)):
            values = []
            print("instance", state_vector[i])
            for j in range(0, len(state_vector[i]["content"])):
                # if the state exists, convert it into binary
                if state_vector[i]["content"][j][0] != 0:
                    values.append({"bin": format(j, 'b'), "scalar": state_vector[i]["content"][j][0]})
            dirac_state_json.append({"content": values, "type": "STATE", "key": i})

        return dirac_state_json

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
    

    def group_gates(num_qubits, circuit):
        print("in_grouped gates")
        gates = circuit.data

        operation_list = []
        operation = []
        qubits_in_operation = []

        current_qubit = 0



        current_gate = gates.pop(0)
        while current_gate != None:
            # current_gate = gates.pop(0)

            # for i in range(0, num_qubits):




            print("CURRENT GATE", current_gate)

            for k in range(0, num_qubits):#len(current_gate.qubits)):
                qubit_overlap = False
                covered_by_gate = False
                print("IN LOOP FOR", k)

                #check if current qubit is already accounted for in column

                if k in qubits_in_operation:
                    print("overlap from if")
                    continue

                #     qubit_overlap = True
                if current_gate != None:
                    for l in range(0, len(current_gate.qubits)):
                        if current_gate.qubits[l].index in qubits_in_operation:
                            qubit_overlap = True
                            print("overlap from else")
                            break

                # if not covered_by_gate:
                    #check if gate applies to qubits
                if not qubit_overlap:
                    print("no qubit overlap")
                    found = False
                    if current_gate != None:
                        # found = False
                        for l in range(0, len(current_gate.qubits)):
                            if current_gate.qubits[l].index == k:
                                print("found")
                                operation.append(current_gate)
                                for m in range(0, len(current_gate.qubits)):

                                    qubits_in_operation.append(current_gate.qubits[m].index)
                                found = True
                                if len(gates) > 0:

                                    current_gate = gates.pop(0)
                                else:
                                    current_gate = None
                                break
                    if not found:
                        print("not found")
                        qubits_in_operation.append(k)
                        operation.append(None)

                    # If qubits overlap happened, append and 
                    if qubit_overlap and not covered_by_gate:
                        print("QUBIT OVERLAP")
                        operation_list.append(operation)
                        operation = []
                        qubits_in_operation = []

        if len(operation) > 0:
            operation_list.append(operation)

        
        print("print operation list", operation_list)

        return operation_list



