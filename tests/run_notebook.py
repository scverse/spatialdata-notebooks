import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import read, write

import re 
import pathlib


def execute_notebook(notebook_path):

    notebook =  read(notebook_path, as_version=4)
    execute_preprocessor = ExecutePreprocessor(timeout=600)  # Set the timeout as needed

    try:
        execute_preprocessor.preprocess(notebook, {'metadata': {'path': '.'}})
    except Exception as e:
        print(f"Error executing notebook: {e}")
        return False

    with open(notebook_path, 'w') as f:
        write(notebook, f)
    
    return True


def update_notebook_interactive_params(notebook_path):
    # Load the Jupyter notebook
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    # Iterate through the cells in the notebook
    for cell in notebook_content.cells:
        if cell.cell_type == 'code':
            # Check if the code cell contains "Interactive("
            if "Interactive(" in cell.source:
                # Check if the parameters are not already present in that line
                if not all(param in cell.source for param in ["tested_notebook=", "test_target=", "take_screenshot="]):
                    # Add the parameters to the code cell source
                    cell.source = cell.source.replace("Interactive(", f'Interactive(tested_notebook="{pathlib.Path(notebook_path).name}", test_target="cell5", take_screenshot=True, ')

    # Save the modified notebook
    with open(notebook_path, 'w', encoding='utf-8') as modified_notebook_file:
        nbformat.write(notebook_content, modified_notebook_file)

    
if __name__ == "__main__":

    notebook_path = "notebooks/examples/test_notebook.ipynb"

    update_notebook_interactive_params(notebook_path)

    if execute_notebook(notebook_path):
        print("Notebook executed successfully")


