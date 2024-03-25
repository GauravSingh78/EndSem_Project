import re



def decimal_to_hex_fraction(decimal_number):
    # Separate the integer and fractional parts
    decimal_number = float(decimal_number)
    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part

    # Convert the integer part to hexadecimal
    hex_integer_part = hex(integer_part)[1:]

    # Convert the fractional part to hexadecimal
    hex_fractional_part = ""
    precision = 4

    for _ in range(precision):
        fractional_part *= 16
        digit = int(fractional_part)
        hex_fractional_part += hex(digit)[2:]
        fractional_part -= digit

    # Combine the hexadecimal integer and fractional parts
    hex_number = f"{hex_integer_part}.{hex_fractional_part}"
    hex_number = hex_number[1:]
    return hex_number

def heximal(num,bit_width):
    return hex(int(float(num) * (2**(bit_width - 1))) & ((1 << bit_width) - 1))[2:]


def convert_floats_to_hexadecimal(condition, bit_width):
    float_pattern = r'\b\d+\.\d+\b'
    float_matches = re.findall(float_pattern, condition)

    # for match in float_matches:
    #     # hex_value = hex(int(float(match) * (2**(bit_width - 1))) & ((1 << bit_width) - 1))[2:]
    #     hex_value = heximal(match,bit_width)
    #     # hex_value = decimal_to_hex_fraction(match)
        
    #     condition = condition.replace(match, f"{hex_value}")
    #     # condition = condition.replace(match, f"{bit_width}'h{hex_value}")

    return condition



def generate_verilog(rules, tree_number):
    module_name = f"RF_model_{tree_number}"
    verilog_code = f"module {module_name}(vinp,vdd,pd);\n\tinput wreal vinp;\n\tinput wreal vdd;\n\tinput wreal pd;\n\treal prediction;\n\nanalog begin\n"


    for i, rule in enumerate(rules):
        condition = rule.replace("return", "").strip()
        condition = condition.replace("and", "&&") 
        condition = condition.replace("temperature", "temp_value") 
        condition = condition.replace(";", "")  
        value = rules[rule]
        

        # Convert float values in conditions to 16-bit hexadecimal using regex
        condition = convert_floats_to_hexadecimal(condition, 16)
        
        # Convert decimal float values to 16-bit hexadecimal
        if '.' in value:
            value = convert_floats_to_hexadecimal(value, 16)
    

        if i == 0:
            verilog_code += f"    if ({condition}) begin\n"
        else:
            verilog_code += f"    else if ({condition}) begin\n"

        verilog_code += f"        prediction = {value};\n"
        verilog_code += "    end\n"

    verilog_code += "    else begin\n"
    verilog_code += "        prediction = 0.0;\n"
    verilog_code += "    end\n"
    verilog_code += "end\nendmodule\n\n"

    return verilog_code




def read_rules_from_file(file_path):
    rules = {}
    with open(file_path, "r") as file:
        lines = file.readlines()

    current_tree_number = None
    current_rules = {}

    for line in lines:
        if "Rules from Tree" in line:
            if current_tree_number is not None:
                rules[current_tree_number] = current_rules
            current_tree_number = int(line.split()[-1])
            current_rules = {}
        elif line.startswith("if"):
            parts = line.split(":")
            condition = parts[0][2:].strip()
            value = parts[1].strip().split()[1]
            current_rules[condition.strip()] = value.strip()

    if current_tree_number is not None:
        rules[current_tree_number] = current_rules

    return rules

rules_file_path = r"C:\Users\ASUS\OneDrive\Desktop\opamp_45_outputs.txt"
all_rules = read_rules_from_file(rules_file_path)

# Generate Verilog modules for each tree
verilog_code = ""
for tree_number, rules in all_rules.items():
    verilog_code += generate_verilog(rules, tree_number)

# Save Verilog modules to a file
with open(r"C:\Users\ASUS\OneDrive\Desktop\opamp_45_verilog(2156).txt", "w") as file:
    file.write(verilog_code)

print("Verilog modules generated and saved to",file.name)



# a = heximal(1.25,16)
# b = heximal(2.05,16)
# c = heximal(1.648,16)
# print(f"{a , b , c}")