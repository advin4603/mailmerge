"""
csv_handler.py : Handles Reading and Writing of .csv files. Used for Getting Data from User.
"""
import csv
from interface import user_error


def csv_namer(template_location):
    """ Changes the extension of template file from ".txt" to ".csv" """
    csv_location = template_location.rstrip("txt") + "csv"
    return csv_location


def csv_writer(var_list, csv_location):
    """Writes Column names in .csv file"""
    with open(csv_location, mode="w") as csv_file:  # Opening the csv file
        csv_file_writer = csv.writer(csv_file)  # Creating a writer object
        csv_file_writer.writerow(var_list)  # Writing a row in the csv file


def csv_reader(var_list, csv_location):
    """ To read the user provided values from the .csv file"""
    row_values = []
    with open(csv_location) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            row_values.append(row)
    if row_values[0] == var_list:
        row_number = 1
        for row in row_values[1:]:
            if len(row) != len(var_list):
                user_error(
                    f"Data not filled completely in row number {row_number} (Row number excluding column headers.)")
                return
            row_number += 1
        return row_values[1:]  # Returns all the row values except the column headers.
    else:
        user_error("ERROR! You Changed The Column Headers.")
