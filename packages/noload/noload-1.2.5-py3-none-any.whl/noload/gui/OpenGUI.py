import tkinter as tk
from tkinter import ttk
from noloadj.gui.gui1 import App as App1
from noloadj.gui.gui2 import App as App2
import xml.etree.ElementTree as ET
import pandas as pd
from ast import literal_eval


def preprocess_xml(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract data from XML
    data = []
    for iteration in root.iter("Iteration"):
        iteration_number = int(iteration.get("Number"))
        is_best_solution = iteration.get("isBestSolution")
        is_solution = iteration.get("isSolution")
        inputs = iteration.find("Inputs")
        outputs = iteration.find("Outputs")

        inputs_data = {input_elem.get("Name"): float(input_elem.get("Value"))
                       for input_elem in inputs.iter("Input")}
        outputs_data = {output_elem.get("Name"): float(output_elem.get("Value"))
                        for output_elem in outputs.iter("Output")}

        iteration_data = {
            "IterationNumber": iteration_number,
            "IsBestSolution": is_best_solution,
            "IsSolution": is_solution,
            **inputs_data,
            **outputs_data
        }
        data.append(iteration_data)

    # Convert data to DataFrame
    df = pd.DataFrame(data)
    option_list = df.columns[3:].values.tolist()

    # Extract specifications from XML
    bounds = root.find("SPECIFICATIONS/BoundsOfInputs")
    objective_functions = root.find("SPECIFICATIONS/ObjectiveFunctions")
    equality_constraints = root.find("SPECIFICATIONS/EqualityConstraints")
    inequality_constraints = root.find("SPECIFICATIONS/InequalityConstraints")
    free_outputs = root.find("SPECIFICATIONS/FreeOutputs")

    all_dfs_array = []

    # Extract bounds
    bounds_data = []
    for bound in bounds.iter("Bounds"):
        bound_name = bound.get("Name")
        bound_value = bound.get("Value")
        bound_in_out = bound.get("Type")
        bounds_data.append(
            {"Name": bound_name, "Value": literal_eval(bound_value),
             "In_Out": bound_in_out})

    df_bounds = pd.DataFrame(bounds_data)
    df_bounds["Type"] = "bounds"

    all_dfs_array.append(df_bounds)

    # Extract objective function data
    objective_functions_data = []
    for obj_func in objective_functions.iter("Objective"):
        objective_name = obj_func.get("Name")
        objective_value = obj_func.get("Value")
        objective_in_out = obj_func.get("Type")
        objective_functions_data.append({"ObjectiveName": objective_name,
                                         "ObjectiveValue": literal_eval(
                                             objective_value),
                                         "In_Out": objective_in_out})

    # Convert objective function data to DataFrame
    df_objective_functions = pd.DataFrame(objective_functions_data)
    df_objective_functions["Type"] = "objective"
    df_objective_functions.columns = ["Name", "Value", "In_Out", "Type"]

    objectives = df_objective_functions["Name"].values

    all_dfs_array.append(df_objective_functions)

    # Extract equality constraint data
    if equality_constraints is not None:
        equality_constraints_data = []
        for eq_constraint in equality_constraints.iter("EqualityConstraint"):
            constraint_name = eq_constraint.get("Name")
            constraint_value = eq_constraint.get("Value")
            constraint_in_out = eq_constraint.get("Type")
            equality_constraints_data.append({"ConstraintName": constraint_name,
                                              "ConstraintValue": literal_eval(
                                                  constraint_value),
                                              "In_Out": constraint_in_out})

        # Convert equality constraint data to DataFrame
        df_equality_constraints = pd.DataFrame(equality_constraints_data)

        df_equality_constraints["Type"] = "eq_cstr"
        df_equality_constraints.columns = ["Name", "Value", "In_Out", "Type"]

        all_dfs_array.append(df_equality_constraints)

    # Extract inequality constraint data
    if inequality_constraints is not None:
        inequality_constraints_data = []
        for ineq_constraint in inequality_constraints.iter(
                "InequalityConstraint"):
            constraint_name = ineq_constraint.get("Name")
            constraint_value = ineq_constraint.get("Value")
            constraint_in_out = ineq_constraint.get("Type")
            inequality_constraints_data.append(
                {"ConstraintName": constraint_name,
                 "ConstraintValue": literal_eval(constraint_value),
                 "In_Out": constraint_in_out})

        # Convert inequality constraint data to DataFrame
        df_inequality_constraints = pd.DataFrame(inequality_constraints_data)

        df_inequality_constraints["Type"] = "ineq_cstr"
        df_inequality_constraints.columns = ["Name", "Value", "In_Out", "Type"]

        all_dfs_array.append(df_inequality_constraints)

    # Extract free output data
    if free_outputs is not None:
        free_outputs_data = []
        for free_output in free_outputs.iter("FreeOutput"):
            output_name = free_output.get("Name")
            free_in_out = free_output.get("Type")
            free_outputs_data.append(
                {"OutputName": output_name, "In_Out": free_in_out})

        # Convert free output data to DataFrame
        df_free_outputs = pd.DataFrame(free_outputs_data)

        df_free_outputs["Type"] = "free"
        df_free_outputs.columns = ["Name", "In_Out", "Type"]

        # Filter out the objectives
        df_free_outputs = df_free_outputs[
            ~df_free_outputs["Name"].isin(objectives)]

        all_dfs_array.append(df_free_outputs)

    specifications_df = pd.DataFrame(
        columns=["Name", "Value", "In_Out", "Type"])

    for i in all_dfs_array:
        specifications_df = pd.concat([specifications_df, i], axis=0)

    specifications_df = specifications_df.set_index('Name')

    return df, option_list, specifications_df, objectives


def openGUI(xml_file_path):

    df, option_list, specifications_df, objectives=preprocess_xml(xml_file_path)

    ### Tk App ###

    root = tk.Tk()
    root.title("Notebook")

    # Create a tabbed interface
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create the first tab and add the App and ImageWindow instances from program1
    tab1 = ttk.Frame(notebook)
    app1 = App1(tab1, option_list, df, specifications_df)
    notebook.add(tab1, text="Plot Variable/Iteration")

    # Create the second tab and add the App and ImageWindow instances from program2
    tab2 = ttk.Frame(notebook)
    app2 = App2(tab2, df)
    app2.update_options(option_list, option_list)
    notebook.add(tab2, text="Plot Variable/Variable")


    root.mainloop()