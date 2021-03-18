"""detector.py : Handles detection of variables used in the template."""
from interface import user_error

opening = "<"
closing = ">"


def detect_var(file_path):
    """Scans the text file and finds variables enclosed in <> (Angular Brackets). 
    Returns a list of all distinct variable names"""

    with open(file_path) as template_file:
        text = template_file.read()

    looking_for_closing = False
    last_opening_index = None
    var_list = []

    for letter_index in range(len(text)):
        letter = text[letter_index]

        if letter == opening:
            # Opening tag of variable found.
            if looking_for_closing:
                # If previous opening tag is not closed then raise error
                user_error("ERROR IN TEMPLATE : (Two Continuous Openings)")

            looking_for_closing = True
            last_opening_index = letter_index

        elif letter == closing:
            # Closing tag of variable found.
            if not looking_for_closing:
                # No tag was opened so raise error.
                user_error("ERROR IN TEMPLATE : (Randomly used closing)")

            var_name = text[last_opening_index + 1:letter_index]

            if var_name not in var_list:
                var_list.append(var_name)

            looking_for_closing = False
            last_opening_index = None

    if looking_for_closing:
        user_error("ERROR IN TEMPLATE : (Did not close opening tag)")

    return var_list
