# Run notebook script

This notebook is used for testing Jupyter notebooks in the spatialdata-notebooks branch. 

## Workflow

The script has three parts:

1. add_test_parameters_to_notebook goes through the cells in the Jupyter notebook and searches for the use of the class Interactive. After it finds one, it edits the cell to add new parameters for testing. The three parameters are: 
    1. _test_notebook_name: the name of the notebook being executed
    2. _notebook_cell_id: Interactive_{count of Interactive in that notebook}, e.g if it's the first instance of Interactive in that notebook, the parameter is set to Interactive_1.
    3. _generate_screenshots: A boolean variable. If set to true, generates screenshots and places it in the folder tests/generated_screenshots/_test_notebook_name/_cell_id

    e.g Interactive(sdata, headless=True) becomes Interactive(sdata, headless=True, _test_notebook_name="notebook_name.ipynb", _cell_id="Interactive_1", _generate_screenshots=True)

2. run_notebook executes the script (which includes the edited Interactive cell) If the _generate_screenshots parameter was True, the screenshots are generated.

3. compare_screenshots checks the folders, generated_screenshots and groundtruth_screenshots, and compares each image.