from run_notebook import add_test_parameters_to_cell


def test_add_parameters_to_cell():
    cell_text = "Interactive(sdata=sdata, headless=True)"
    expected_text = 'Interactive(sdata=sdata, headless=True, _test_notebook_name="test_notebook.ipynb", _notebook_cell_id="Interactive_1", _generate_screenshots=True)'

    assert (
        add_test_parameters_to_cell(cell_text, "test_notebook.ipynb", '"Interactive_1"', generate_screenshots=True)
        == expected_text
    )


def test_add_parameters_to_cell_no_interactive():
    cell_text = "print('Hello world')"
    expected_text = cell_text

    assert (
        add_test_parameters_to_cell(cell_text, "test_notebook.ipynb", '"Interactive_1"', generate_screenshots=True)
        == expected_text
    )


def test_add_parameters_to_cell_generate_screenshots_is_false():
    cell_text = "Interactive(sdata=sdata, headless=True)"
    expected_text = 'Interactive(sdata=sdata, headless=True, _test_notebook_name="test_notebook.ipynb", _notebook_cell_id="Interactive_1", _generate_screenshots=False)'

    assert (
        add_test_parameters_to_cell(cell_text, "test_notebook.ipynb", '"Interactive_1"', generate_screenshots=False)
        == expected_text
    )


def test_add_parameters_to_cell_screenshot_overwrite():
    cell_text = 'Interactive(sdata=sdata, headless=True,  _test_notebook_name="test_notebook.ipynb", _notebook_cell_id="Interactive_1", _generate_screenshots=False)'
    expected_text = 'Interactive(sdata=sdata, headless=True, _test_notebook_name="test_notebook.ipynb", _notebook_cell_id="Interactive_1", _generate_screenshots=True)'

    assert (
        add_test_parameters_to_cell(cell_text, "test_notebook.ipynb", '"Interactive_1"', generate_screenshots=True)
        == expected_text
    )