# import numpy as np

# def evaluate_all_conditions(vinp, pd, vdd):
#     results = []

#     function_file_path = r"C:\Users\ASUS\OneDrive\Desktop\out.py" 

    
#     with open(function_file_path, 'r') as file:
#         functions_code = file.read()

    
#     for i in range(100):  
#         function_name = f"decision_tree_rule_{i}"
#         exec(functions_code)  
#         function = locals()[function_name] 
#         result = function(vinp, pd, vdd) or 0  
#         results.append(result)

#     return results


# vinp_value = 1.5
# pd_value = 1.8
# vdd_value = 3.8
# result_list = evaluate_all_conditions(vinp_value, pd_value, vdd_value)
# print("Length",len(result_list))
# print("Results:", result_list)
# print(np.average(result_list))

#######################################################################################


import numpy as np
import pickle

def import_set(file_path):
    with open(file_path, 'rb') as file:
        my_set = pickle.load(file)
    return my_set

import_file_path = r'exported_set.pkl'


def evaluate_all_conditions(**kwargs):
    results = []

    function_file_path = r"TreeFunction.py"

    with open(function_file_path, 'r') as file:
        functions_code = file.read()

    for i in range(1,21):
        function_name = f"decision_tree_rule_{i}"
        exec(functions_code)
        function = locals()[function_name]
        result = function(**kwargs) or 0
        results.append(result)

    return results


input_parameters = import_set(import_file_path)

print("Imported Set:", input_parameters)

vinp_value = 1.638227 
pd_value = 3.0
vdd_value = 3.0
process_value = 3
temperature_value = 85
input_values = {'vinp': vinp_value, 'pd': pd_value, 'vdd': vdd_value, 'process':process_value,'temperature':temperature_value}

result_list = evaluate_all_conditions(**input_values)

print("Length:", len(result_list))
print("Results:", result_list)
print("Average:", np.average(result_list))
