# Your source code should be in a plain text file called 'code.txt' in the same directory as the compiler file.
# The output file is called hex_code, and contains the hex version of the instructions to be imported into logisim.
# Important: for the reset button to work properly, the first line of code should be a label or a none instruction.


OPCODES = {
    "none": "00000",
    "label": "00000",
    "branch": "00001",
    "store": "00010",
    "load": "00011",
    "halt": "00100",
    "set": "11110",
    "copy": "11111",
    "compare": "10000",
    "add": "10001",
    "subtract": "10010",
    "lowmul": "10011",
    "highmul": "10100",
    "divide": "10101",
    "modulo": "10110",
    "and": "10111",
    "or": "11000",
    "not": "11001",
    "xor": "11010",
    "lshift": "11011",
    "rshift": "11100",
    "arshift": "11101"
}

BRANCH_CONDITION_CODES = {
    "gt": "000",
    "gte": "001",
    "eq": "010",
    "lt": "011",
    "lte": "100",
    "al": "110",
    "ne": "111",
}

class CompileError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
        
label_indexes = {} # Maps labels to their line index so that their instruction addresses can be stored
line_index = 0 # Line index of current line of code
compiled_code = "" # Stores the complete compiled code.
comparison_happened = False # Is set to true after a comparison. Used to check if a user uses branch without comparison first.

def none(compiled_code):
    compiled_code += "0"*24+"\n"
    return compiled_code


def label(line, line_index, compiled_code): # Labels are stored as none operations (they do nothing)
    instruction = line.strip().split(" ")
    label_name = instruction[0]
    if len(instruction) > 1 or label_name == "" or label_name[-1] != ":" or label_name == ":":
        raise CompileError(f"Line not recognized as an opcode or label on line {line_index+1}\n"
                           "Remember labels must be one word with at least one character (no spaces) and be followed by a comma.")
    elif label_name[0:-1] in label_indexes:
        raise CompileError(f"This label already exists, on line {line_index+1}.")
    label_without_colon = label_name[0:-1]
    label_indexes[label_without_colon] = line_index
    compiled_code += "0"*24+"\n"
    return compiled_code
    

def branch(line, line_index, compiled_code, comparison_happened):
    instruction = line.strip().split(" ")
    if len(instruction) != 3:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           "A branch instruction should include two operands: branch <condition> <label>.")
    elif comparison_happened == False:
        raise CompileError(f"You attempted to use a branch operation without previous comparison on line {line_index+1}.")
    elif (branch_condition := instruction[1]) not in BRANCH_CONDITION_CODES:
        raise CompileError(f"Your branch condition was not recognised on line {line_index+1}. Valid branch conditions are:\n"
                           "    - gt (greater than)\n"
                           "    - gte (greater than or equal to)\n"
                           "    - eq (equal to)\n"
                           "    - lt (less than)\n"
                           "    - lte (less than or equal to)\n"
                           "    - al (always, branch always happens)\n")
    elif (label := instruction[2]) not in label_indexes:
        raise CompileError(f"The label used in your branch instruction was not recognised on line {line_index+1}.")
    
    label_index = label_indexes[label]
    label_address = bin(int(label_index))[2:].zfill(16)
    branch_code = BRANCH_CONDITION_CODES[branch_condition]
    
    compiled_code += OPCODES["branch"] + branch_code + label_address + "\n"
    return compiled_code
    
    
def store(line, line_index, compiled_code):
    instruction = line.strip().split(" ")
    if len(instruction) != 3:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           "A store instruction should include two operands: store Rn <memory_location>.")
    elif len(instruction[1]) != 2 or instruction[1][0].lower() != "r" or not instruction[1][1].isdigit() or int(instruction[1][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the first operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif not instruction[2].isnumeric():
        raise CompileError(f"An incorrect memory address was entered on line {line_index+1} on the second operand.\n"
                           "Remember a memory address should be an integer, n, where 0 ≤ n ≤ 65535")
    elif int(instruction[2]) > 65535:
        raise CompileError(f"A memory address that is too large was entered on line {line_index+1} on the second operand.\n"
                           "Memory only supports addresses between 0 and 65535 inclusive.")
        
    register_code = bin(int(instruction[1][1]))[2:].zfill(3)
    memory_address_code = bin(int(instruction[2]))[2:].zfill(16)
    compiled_code += OPCODES["store"] + register_code + memory_address_code + "\n"
    return compiled_code
    
    
def load(line, line_index, compiled_code):
    instruction = line.strip().split(" ")
    if len(instruction) != 3:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           "A load instruction should include two operands: store Rn <memory_location>.")
    elif len(instruction[1]) != 2 or instruction[1][0].lower() != "r" or not instruction[1][1].isdigit() or int(instruction[1][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the first operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif not instruction[2].isnumeric():
        raise CompileError(f"An incorrect memory address was entered on line {line_index+1} on the second operand.\n"
                           "Remember a memory address should be an integer, n, where 0 ≤ n ≤ 65535")
    elif int(instruction[2]) > 65535:
        raise CompileError(f"A memory address that is too large was entered on line {line_index+1} on the second operand.\n"
                           "Memory only supports addresses between 0 and 65535 inclusive.")
        
    register_code = bin(int(instruction[1][1]))[2:].zfill(3)
    memory_address_code = bin(int(instruction[2]))[2:].zfill(16)
    compiled_code += OPCODES["load"] + register_code + memory_address_code + "\n"
    return compiled_code
    

def halt(compiled_code):
    compiled_code += OPCODES["halt"] + "0"*19 + "\n"
    return compiled_code
    
    
def compare(line, line_index, compiled_code, comparison_happened):
    instruction = line.strip().split(" ")
    if len(instruction) != 3:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           "A compare instruction should include two operands: compare Rn Ra.")
    elif len(instruction[1]) != 2 or instruction[1][0].lower() != "r" or not instruction[1][1].isdigit() or int(instruction[1][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the first operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif len(instruction[2]) != 2 or instruction[2][0].lower() != "r" or not instruction[2][1].isdigit() or int(instruction[2][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the second operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    
    register_code_1 = bin(int(instruction[1][1]))[2:].zfill(3)
    register_code_2 = bin(int(instruction[2][1]))[2:].zfill(3)
    compiled_code += OPCODES["compare"] + "000" + register_code_1 + register_code_2 + "0"*10 + "\n"
    comparison_happened = True
    return compiled_code, comparison_happened
    
    
def alu_operation(line, line_index, compiled_code):
    instruction = line.strip().split(" ")
    if len(instruction) != 4:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           f"A {instruction[0]} instruction should include three operands: {instruction[0]} Rn Ra Rb.")
    elif len(instruction[1]) != 2 or instruction[1][0].lower() != "r" or not instruction[1][1].isdigit() or int(instruction[1][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the first operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif len(instruction[2]) != 2 or instruction[2][0].lower() != "r" or not instruction[2][1].isdigit() or int(instruction[2][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the second operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif len(instruction[3]) != 2 or instruction[3][0].lower() != "r" or not instruction[3][1].isdigit() or int(instruction[3][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the third operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    
    register_code_1 = bin(int(instruction[1][1]))[2:].zfill(3)
    register_code_2 = bin(int(instruction[2][1]))[2:].zfill(3)
    register_code_3 = bin(int(instruction[3][1]))[2:].zfill(3)
    compiled_code += OPCODES[instruction[0]] + register_code_1 + register_code_2 + register_code_3 + "0"*10 + "\n"
    return compiled_code


def op_set(line, line_index, compiled_code):
    instruction = line.strip().split(" ")
    if len(instruction) != 3:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           "A load instruction should include two operands: store Rn <memory_location>.")
    elif len(instruction[1]) != 2 or instruction[1][0].lower() != "r" or not instruction[1][1].isdigit() or int(instruction[1][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the first operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif not ((instruction[2][0] == "-" and len(instruction[2]) > 1 and instruction[2][1:].isnumeric()) or instruction[2].isnumeric()):
        raise CompileError(f"The value of the second operand on line {line_index+1} was not recognised as a number.\n"
                           "Remember that a set operation takes a numerical value as its second operand.")
    elif int(instruction[2]) > 32767 or int(instruction[2]) < -32768:
        raise CompileError(f"The value of the second operand on line {line_index+1} is out of bounds."
                           "Remember that a register can only take values between -32768 and 32767 inclusive.")
    
    register_code = bin(int(instruction[1][1]))[2:].zfill(3)
    value = int(instruction[2])
    if value >= 0:
        binary_value = bin(value)[2:].zfill(16)
    else:
        binary_value = bin(abs(value+1))[2:].zfill(16)
        binary_value = "".join([str(1-int(i)) for i in binary_value])
        

    compiled_code += OPCODES["set"] + register_code + binary_value + "\n"
    return compiled_code
        

def copy(line, line_index, compiled_code):
    instruction = line.strip().split(" ")
    if len(instruction) != 3:
        raise CompileError(f"An incorrect number of operands were inputted on line {line_index+1}.\n"
                           "A compare instruction should include two operands: compare Rn Ra.")
    elif len(instruction[1]) != 2 or instruction[1][0].lower() != "r" or not instruction[1][1].isdigit() or int(instruction[1][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the first operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
    elif len(instruction[2]) != 2 or instruction[2][0].lower() != "r" or not instruction[2][1].isdigit() or int(instruction[2][1]) > 7:
        raise CompileError(f"An incorrect register reference code was entered on line {line_index+1} on the second operand.\n"
                           "A register reference code should be 'Rn', where n is a digit between 0 and 7.")
        
    register_code_1 = bin(int(instruction[1][1]))[2:].zfill(3)
    register_code_2 = bin(int(instruction[2][1]))[2:].zfill(3)
    compiled_code += OPCODES["copy"] + register_code_1 + register_code_2 + "0"*12 + "\n"
    return compiled_code

source_code = open("code.txt", "r").readlines()

for line in source_code:
    line = line.strip()
    instruction = line.split(" ")[0]
    if instruction == "none": compiled_code = none(compiled_code)
    elif instruction == "branch": compiled_code = branch(line, line_index, compiled_code, comparison_happened)
    elif instruction == "store": compiled_code = store(line, line_index, compiled_code)
    elif instruction == "load": compiled_code = load(line, line_index, compiled_code)
    elif instruction == "halt": compiled_code = halt(compiled_code)
    elif instruction == "compare": compiled_code, comparison_happened = compare(line, line_index, compiled_code, comparison_happened)
    elif instruction == "set": compiled_code = op_set(line, line_index, compiled_code)
    elif instruction == "copy": compiled_code = copy(line, line_index, compiled_code)
    elif instruction in ["add", "sub", "lowmul", "highmul", "div", "mod", "and", "or", "not", "xor", "lshift", "rshift", "arshift"]:
        compiled_code = alu_operation(line, line_index, compiled_code)
    else: compiled_code = label(line, line_index, compiled_code)
    line_index += 1
    
hex_file = open("hex_code", "w")
hex_code = "v2.0 raw\n"
for line in compiled_code[:-1].split("\n"):
    hex_line = "".join([hex(int(line[i:i+4], 2))[2:] for i in range(0, 24, 4)])
    hex_code += hex_line + " "
    
hex_code = hex_code[:-1]
hex_file.write(hex_code)
hex_file.close()
print("Compile successful.")
