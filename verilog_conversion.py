import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.tree import _tree
import numpy as np
import pickle

def get_rules(tree, feature_names, class_names):
    try:
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        paths = []
        path = []

        def recurse(node, path, paths):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                p1, p2 = list(path), list(path)
                p1 += [f"({name} <= {np.round(threshold, 3)})"]
                recurse(tree_.children_left[node], p1, paths)
                p2 += [f"({name} > {np.round(threshold, 3)})"]
                recurse(tree_.children_right[node], p2, paths)
            else:
                path += [(tree_.value[node], tree_.n_node_samples[node])]
                paths += [path]

        recurse(0, path, paths)

        samples_count = [p[-1][1] for p in paths]
        ii = list(np.argsort(samples_count))
        paths = [paths[i] for i in reversed(ii)]

        rules = []
        for path in paths:
            rule = "if "

            for p in path[:-1]:
                if rule != "if ":
                    rule += " and "
                rule += str(p)
            
            if class_names is None:
                rule += ": return " + str(np.round(path[-1][0][0][0], 5))
            else:
                classes = path[-1][0][0]
                l = np.argmax(classes)
                rule += f"class: {class_names[l]} (proba: {np.round(1000.0 * classes[l] / np.sum(classes), 3)}%)"

            rules += [rule]

        return rules
    except (AttributeError, NameError) as e:
        print(f"Error extracting rules: {e}")
        return None


def get_all_rules(forest, feature_names, class_names):
    all_rules = []
    for tree in forest.estimators_:
        rules = get_rules(tree, feature_names, class_names)
        if rules:
            all_rules.append(rules)
    return all_rules



# Load the model
with open(r"C:\Users\ASUS\OneDrive\Desktop\fastnfastp\Test_model.pkl", 'rb') as file:
    model_data = pickle.load(file)

loaded_model = model_data['model']

feature_names = model_data['feature_names']

print("Random Forest Regressor model loaded successfully.")
    
  
class_names = None  

# Extract rules from the Random Forest
all_rules = get_all_rules(loaded_model, feature_names, class_names)

# Print the extracted rules
for i, tree_rules in enumerate(all_rules):
    print(f"\nRules from Tree {i+1}")
    for rule in tree_rules:
        print(rule)

# Write rules to a file if needed
with open(r'C:\Users\ASUS\OneDrive\Desktop\opamp_45_outputs.txt', 'w') as file:
    file.write(f"\nRules from Tree 1\n")
    for i, tree_rules in enumerate(all_rules):
        # file.write(f"\nRules from Tree {i+1}\n")
        for rule in tree_rules:
            file.write(rule + '\n')

print(f"Rules have been extracted and written to {file.name}")
    

