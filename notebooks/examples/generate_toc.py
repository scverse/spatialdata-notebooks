"""Generate a TOC for a notebook."""

# adapted from a user contribution of the user "efueyo" from https://discourse.jupyter.org/t/how-can-i-see-the-table-of-contents-at-the-beginning-of-the-notebook-in-jupyter-lab/19791
# which is licensed under CC BY-NC-SA 3.0 DEED

import json
import urllib.parse


def _generate_toc(notebook_path, indent_char="&emsp;&emsp;"):
    is_markdown = lambda it: "markdown" == it["cell_type"]
    is_title = lambda it: it.strip().startswith("#") and it.strip().lstrip("#").lstrip()

    with open(notebook_path) as in_f:
        nb_json = json.load(in_f)

    toc_numbers = []  # Lista para llevar el conteo de los números de contenido en cada nivel

    for cell in filter(is_markdown, nb_json["cells"]):
        for line in filter(is_title, cell["source"]):
            line = line.strip()
            title = line.lstrip("#").lstrip()

            level = line.count("#")  # Nivel del título según la cantidad de "#"

            if level > len(toc_numbers):
                toc_numbers.append(1)  # Agregar un nuevo nivel con numeración inicial en 1
            else:
                toc_numbers[level - 1] += 1  # Incrementar el número de contenido en el nivel actual
                toc_numbers[level:] = [1] * (len(toc_numbers) - level)  # Reiniciar numeración en niveles inferiores

            toc_number_str = ".".join(str(num) for num in toc_numbers[:level])
            indent = indent_char * level
            url = urllib.parse.quote_plus(title.replace(" ", "-"))
            toc_number_str = " &#x2022; "
            if level > 1:
                indent = indent[len(indent_char) * 2 :]
                out_line = f"{indent}{toc_number_str} [{title}](#{url})<br>\n"
                print(out_line, end="")


if __name__ == "__main__":
    path = "tables.ipynb"
    _generate_toc(path)
