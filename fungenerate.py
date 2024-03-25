
# def generate_python_code_from_pseudocode(pseudocode_lines):
#     python_code = ""
#     for i in range(0, len(pseudocode_lines), 16):
#         code_block = "\n".join(pseudocode_lines[i:i+16])
#         python_code += f"\ndef decision_tree_rule_{i//16}(vinp, pd, vdd):" + "\n"
        
#         indented_code_block = "    " + code_block.replace('\nif ', '\n    if ').replace('then return', ':\n        return')
        
        
#         python_code += f"{indented_code_block}" + "\n"
#     return python_code

# file_path = r"C:\Users\ASUS\OneDrive\Desktop\output.txt"  # Replace with the actual file path
# with open(file_path, 'r') as file:
#     pseudocode_lines = file.readlines()


# python_code = generate_python_code_from_pseudocode(pseudocode_lines)


# output_file_path = r"C:\Users\ASUS\OneDrive\Desktop\out.py"  # Replace with the desired file path
# with open(output_file_path, 'w') as code_file:
#     code_file.write(python_code)

# print(f"Python code has been saved to: {output_file_path}")




##############################################################################

# def generate_python_code_from_pseudocode(pseudocode_lines):
#     python_code = ""
#     rule_count = 1
#     capture_lines = False

#     for line in pseudocode_lines:
#         if f"Rules from Tree {rule_count}" in line:
#             python_code += f"\ndef decision_tree_rule_{rule_count}(vinp, pd, vdd):" + "\n"
#             rule_count += 1
#             capture_lines = True

#         elif capture_lines and line.strip():  # Start capturing lines after the first rule
#             indented_code_block = "    " + line.replace('return', ':\n        return')
#             python_code += f"{indented_code_block}" + "\n"

#     return python_code

# # Read pseudocode from file
# file_path = r"C:\Users\ASUS\OneDrive\Desktop\outs.txt"  # Replace with the actual file path
# with open(file_path, 'r') as file:
#     pseudocode_lines = file.readlines()

# # Generate Python code
# python_code = generate_python_code_from_pseudocode(pseudocode_lines)

# # Save Python code to a file
# output_file_path = r"C:\Users\ASUS\OneDrive\Desktop\oute.py"  # Replace with the desired file path
# with open(output_file_path, 'w') as code_file:
#     code_file.write(python_code)

# print(f"Python code has been saved to: {output_file_path}")



##########################################################################################################################

# def generate_python_code_from_pseudocode(pseudocode_lines, input_parameters):
#     python_code = ""
#     rule_count = 1
#     capture_lines = False

#     for line in pseudocode_lines:
#         if f"Rules from Tree {rule_count}" in line:
#             python_code += f"\ndef decision_tree_rule_{rule_count}({', '.join(input_parameters)}):" + "\n"
#             rule_count += 1
#             capture_lines = True

#         elif capture_lines and line.strip():  # Start capturing lines after the first rule
#             indented_code_block = "    " + line.replace('return', ':\n        return')
#             python_code += f"{indented_code_block}" + "\n"

#     return python_code

# # Define input parameters as a set
# input_parameters = {'vinp', 'pd', 'vdd'}

# # Read pseudocode from file
# file_path = r"C:\Users\ASUS\OneDrive\Desktop\outs.txt"  # Replace with the actual file path
# with open(file_path, 'r') as file:
#     pseudocode_lines = file.readlines()

# # Generate Python code
# python_code = generate_python_code_from_pseudocode(pseudocode_lines, input_parameters)

# # Save Python code to a file
# output_file_path = r"C:\Users\ASUS\OneDrive\Desktop\oute.py"  # Replace with the desired file path
# with open(output_file_path, 'w') as code_file:
#     code_file.write(python_code)

# print(f"Python code has been saved to: {output_file_path}")


#############################################################################

import pickle

def import_set(file_path):
    with open(file_path, 'rb') as file:
        my_set = pickle.load(file)
    return my_set

import_file_path = r'C:\Users\ASUS\OneDrive\Desktop\New folder\exported_set.pkl'


def generate_python_code_from_pseudocode(pseudocode_lines, input_parameters):
    python_code = ""
    rule_count = 1
    capture_lines = False

    for line in pseudocode_lines:
        if f"Rules from Tree {rule_count}" in line:
            parameter_string = ', '.join(f"{param}=None" for param in input_parameters)
            python_code += f"\ndef decision_tree_rule_{rule_count}({parameter_string}):" + "\n"
            rule_count += 1
            capture_lines = True

        elif capture_lines and line.strip():  
            indented_code_block = "    " + line.replace('return', '\n        return')
            python_code += f"{indented_code_block}" + "\n"

    return python_code


input_parameters = import_set(import_file_path)
print("Imported Set:", input_parameters)

file_path = r"C:\Users\ASUS\OneDrive\Desktop\New folder\output.txt" 
with open(file_path, 'r') as file:
    pseudocode_lines = file.readlines()


python_code = generate_python_code_from_pseudocode(pseudocode_lines, input_parameters)
print("Python Code generated")

output_file_path = r"C:\Users\ASUS\OneDrive\Desktop\New folder\fun.py"  
with open(output_file_path, 'w') as code_file:
    code_file.write(python_code)

print(f"Python code has been saved to: {output_file_path}")
