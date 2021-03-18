"""input_func.py: Handles most of User Input"""

import tkinter as tk
from tkinter import filedialog
from interface import open_file


def inp_template():
    """Asks user for template file location."""

    # Get access to the root window created by tkinter
    root = tk.Tk()

    # Makes Sure the file dialog draws on top of all windows.
    root.attributes("-topmost", True)
    root.lift()

    # Hides the root window
    root.withdraw()

    # Creates a file dialog box.
    location = filedialog.askopenfilename(title="Select Your Template File",
                                          filetypes=(("Text Files", "*.txt"),))
    if location:
        return location
    return


def sql_prompt():
    """Asks user whether to save data in MySQL"""
    choice = input('Do you want to save the data in a MySQL Database?    (Y/N)\n>')
    if choice.lower() == 'y':
        username = input('Enter MySQL username:')
        password = input('Enter MySQL password:')
        return username, password
    else:
        return


def user_csv_prompter(location):
    """Asks user to fill details in the .csv file """
    print('Fill in the details in the file:', location)

    # Opens .csv file in default editor.
    open_file(location)

    input("Press any key to continue.")


def inp_save_folder():
    """Asks user for output save location"""
    # Get access to the root window created by tkinter
    root = tk.Tk()

    # Makes Sure the file dialog draws on top of all windows.
    root.attributes("-topmost", True)
    root.lift()

    # Hides the root window
    root.withdraw()

    # Creates a folder dialog box.
    location = filedialog.askdirectory(parent=root, title="Where To Save Output?")
    if location:
        return location
    return
