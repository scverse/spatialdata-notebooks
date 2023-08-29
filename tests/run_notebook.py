import re

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import read


def execute_notebook(notebook_path) -> None:
    notebook = read(notebook_path, as_version=4)
    execute_preprocessor = ExecutePreprocessor(timeout=600)

    execute_preprocessor.preprocess(notebook, {"metadata": {"path": "."}})


def add_parameters_to_cell(cell, take_screenshot):
    # TODO: Change hardcoded values to variables
    parameters = {
        "coordinate_system_name": '"global"',
        "_tested_notebook": '"test_notebook.ipynb"',
        "_test_target": '"cell5"',
        "_take_screenshot": take_screenshot,
    }

    match = re.search(r"Interactive\((.*?)\)", cell)
    updated_string = cell

    if match:
        # Extract the content within the parentheses
        inner_content = match.group(1)

        # Split the inner content by commas and strip whitespace
        param_list = [param.strip() for param in inner_content.split(",")]

        # Iterate through the parameters and update their values if they exist
        for param, default_value in parameters.items():
            found = False

            # Check if the parameter exists in the list
            for i, item in enumerate(param_list):
                if param in item:
                    # Update the parameter's value to False
                    param_list[i] = f"{param}={default_value}"
                    found = True

            # If the parameter was not found, add it with the default value
            if not found:
                param_list.append(f"{param}={default_value}")

        # Reconstruct the modified inner content
        modified_inner_content = ", ".join(param_list)

        # Create the updated "Interactive()" string
        updated_string = f"Interactive({modified_inner_content})"

        print("Updated command: ", updated_string)

    return updated_string


def update_notebook_interactive_parameters(notebook_path, take_screenshot: bool = False) -> None:
    print("Taking screenshot: ", str(take_screenshot))
    # Load the Jupyter notebook
    with open(notebook_path, encoding="utf-8") as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    # Iterate through the cells in the notebook
    for cell in notebook_content.cells:
        if cell.cell_type == "code":
            # TODO: Add check for Interacitve here? so function isn't called after every cell
            cell.source = add_parameters_to_cell(cell.source, take_screenshot)

    # Save the modified notebook
    with open(notebook_path, "w", encoding="utf-8") as modified_notebook_file:
        nbformat.write(notebook_content, modified_notebook_file)


if __name__ == "__main__":
    notebook_path = "notebooks/examples/test_notebook.ipynb"
    update_notebook_interactive_parameters(notebook_path, take_screenshot=True)
    execute_notebook(notebook_path)
