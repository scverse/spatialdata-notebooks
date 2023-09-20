import os
import re

import nbformat
from matplotlib.testing.compare import compare_images
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import read


def execute_notebook(notebook_path) -> None:
    notebook = read(notebook_path, as_version=4)
    execute_preprocessor = ExecutePreprocessor(timeout=1800)

    execute_preprocessor.preprocess(notebook, {"metadata": {"path": "."}})


def extract_notebook_name(file_path) -> str:
    path_parts = file_path.split("/")
    notebook_name = path_parts[-1]

    return notebook_name


def add_parameters_to_cell(cell, notebook_name, test_target, take_screenshot):
    parameters = {
        "_tested_notebook": '"' + notebook_name + '"',
        "_test_target": test_target,
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
    print("Take screenshot: ", str(take_screenshot))

    # Load the Jupyter notebook
    with open(notebook_path, encoding="utf-8") as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    interactive_count = 1
    notebook_name = extract_notebook_name(notebook_path)

    # Iterate through the cells in the notebook
    for cell in notebook_content.cells:
        if cell.cell_type == "code":
            if re.search(r"Interactive\((.*?)\)", cell.source):
                test_target = '"interactive_' + str(interactive_count) + '"'
                cell.source = add_parameters_to_cell(cell.source, notebook_name, test_target, take_screenshot)
                interactive_count += 1

    # Save the modified notebook
    with open(notebook_path, "w", encoding="utf-8") as modified_notebook_file:
        nbformat.write(notebook_content, modified_notebook_file)


def compare_image_folders(groundtruth_folder, generated_folder):
    print("Comparing images in folders: ", groundtruth_folder, generated_folder)

    # Get images in groundtruth_folder
    groundtruth_images = os.listdir(groundtruth_folder)

    # Get images in generated_folder
    generated_images = os.listdir(generated_folder)

    # Compare images
    for groundtruth_image in groundtruth_images:
        if groundtruth_image in generated_images:
            print("Comparing image: ", groundtruth_image)
            compare_images(
                groundtruth_folder + "/" + groundtruth_image, generated_folder + "/" + groundtruth_image, tol=0.01
            )
        else:
            print("Image not found: ", groundtruth_image)


def compare_screenshots(notebook_path):
    # Check for notebook_path name in generated_screenshots folder

    notebook_name = extract_notebook_name(notebook_path)

    if os.path.exists("tests/groundtruth_screenshots/" + notebook_name):
        groundtruth_screenshots_path = "tests/groundtruth_screenshots/" + notebook_name
        groundtruth_screenshots = os.listdir(groundtruth_screenshots_path)

        test_targets = list(groundtruth_screenshots)

        for test_target in test_targets:
            # Search if test_target exists in generated_screenshots folder
            if os.path.exists("tests/generated_screenshots/" + notebook_name + "/" + test_target):
                compare_image_folders(
                    "tests/generated_screenshots/" + notebook_name + "/" + test_target,
                    "tests/groundtruth_screenshots/" + notebook_name + "/" + test_target,
                )

    else:
        print("No groundtruth screenshots folder found for notebook: ", notebook_name)


if __name__ == "__main__":
    # notebook_path = "notebooks/examples/test_notebook.ipynb"
    # notebook_path = "notebooks/examples/transformations.ipynb"
    # notebook_path = "notebooks/examples/napari_rois.ipynb"
    notebook_path = "notebooks/examples/aggregation.ipynb"

    update_notebook_interactive_parameters(notebook_path, take_screenshot=True)
    execute_notebook(notebook_path)
    compare_screenshots(notebook_path)
