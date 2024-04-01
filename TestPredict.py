import numpy as np
import pickle
import concurrent.futures

def import_set(file_path):
    with open(file_path, 'rb') as file:
        my_set = pickle.load(file)
    return my_set

def evaluate_function(function_code, kwargs):
    exec(function_code)
    results = []
    for i in range(1, 21):
        function_name = f"decision_tree_rule_{i}"
        function = locals()[function_name]
        result = function(**kwargs) or 0
        results.append(result)
    return results

def evaluate_all_conditions_parallel(input_parameters, function_code):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_param = {executor.submit(evaluate_function, function_code, params): params for params in input_parameters}
        for future in concurrent.futures.as_completed(future_to_param):
            params = future_to_param[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"Function execution generated an exception: {exc}")
                results.append([])  # Append empty list as placeholder for failed execution
    return results

import_file_path = r'exported_set.pkl'
function_file_path = r"TreeFunction.py"

input_parameters = import_set(import_file_path)
vinp_value = 1.638227 
pd_value = 3.0
vdd_value = 3.0
process_value = 3
temperature_value = 85
input_values = {'vinp': vinp_value, 'pd': pd_value, 'vdd': vdd_value, 'process': process_value, 'temperature': temperature_value}

with open(function_file_path, 'r') as file:
    functions_code = file.read()

# Convert input_parameters to a list of dictionaries
input_parameters_list = [input_values] * len(input_parameters)

result_list = evaluate_all_conditions_parallel(input_parameters_list, functions_code)

print("Length:", len(result_list))
print("Results:", result_list)
print("Average:", np.nanmean(result_list))
