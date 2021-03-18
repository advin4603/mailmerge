"""substituter.py : Handles Substitution of variables with their respective values."""

import os.path


def substitute(var_list, data, template_location, save_location):
    """Substitutes variables with their respective values."""
    with open(template_location) as template_file:
        template_text = template_file.read()

    row_number = 1
    for row in data:
        new_text = template_text
        for var, sub in zip(var_list, row):
            new_text = new_text.replace("<" + var + ">", sub)
        with open(os.path.join(save_location, f"{row_number}.txt"), "w") as out_file:
            out_file.write(new_text)
        row_number += 1
