"""interface.py: Handles most of the interaction with user."""
import subprocess
import sys
import time
import os


def print_header():
    """Prints the name of the program."""
    print("..Mail Merge..")


def print_instructions():
    """Displays instructions."""
    with open("instructions.txt") as instructions_file:
        print(instructions_file.read())
    input("Press Any Key to Continue...")


def user_error(error):
    """Handles User's Errors"""

    # print the User's error in the error stream.
    sys.stderr.write(error)

    # Give a time gap to make sure error is printed before the quit message.
    time.sleep(0.5)

    # Makes sure quit message is printed in a new line.
    print()
    quit_program()


def program_error(traceback):
    """Handles program errors."""

    # Gets Current date and time in a format that can be used in a filename.
    current_time = time.strftime("%Y%m%d-%H%M%S")

    # Generate filename and filepath.
    file_name = "traceback_" + current_time + ".txt"
    if not os.path.exists("Tracebacks"):
        os.mkdir("Tracebacks")
    file_path = os.path.join(os.getcwd(), "Tracebacks", file_name)

    # Save error in traceback file.
    with open(file_path, "w") as error_file:
        error_file.write(traceback)

    print("Something Went Wrong..")
    print(f"See {file_path} for details.")
    quit_program()


def quit_program():
    """Quits the program."""
    input("Press any key to quit...")
    exit()


def open_file(file_path):
    """Opens file in default program. Opens explorer in case a folder path is provided."""
    if sys.platform == "win32":
        # For Windows.
        os.startfile(file_path)
    else:
        # Other OS like MacOS and Unix-like systems (Linux, FreeBSD, Solaris...)
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, file_path])
