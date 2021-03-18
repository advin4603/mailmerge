"""main.py : Consists of the main program."""
import csv_handler
import detector
import input_func
import interface
import sql_func
import substituter
import time
import traceback


def main():
    """Runs the main Mail Merge Program."""
    interface.print_header()
    time.sleep(1)
    interface.print_instructions()

    template_location = input_func.inp_template()
    if template_location is None:
        interface.quit_program()
    var_list = detector.detect_var(template_location)
    var_list.sort()
    print("Successfully loaded template.")
    time.sleep(0.5)

    sql_access = sql_func.sql_access_prompt()

    if sql_access is not None:
        # Use Data In MySQL Database
        table_name, sql_connection = sql_access
        if not sql_func.verify_data(sql_connection, var_list, table_name):
            interface.user_error("The Table does not contain all the variables used in your template.")

        data = sql_func.data_getter(sql_connection, table_name, var_list)
        print("Successfully Loaded Data")
        time.sleep(0.5)

    else:
        # Get User Data
        csv_location = csv_handler.csv_namer(template_location)
        csv_handler.csv_writer(var_list, csv_location)
        input_func.user_csv_prompter(csv_location)
        data = csv_handler.csv_reader(var_list, csv_location)
        print("Successfully Loaded Data")
        time.sleep(0.5)

        sql_prompt = input_func.sql_prompt()
        if sql_prompt is not None:
            # Save User Data
            username, password = sql_prompt
            sql_connection = sql_func.sql_connect(username, password)
            sql_func.database_creator(sql_connection)
            table_name = sql_func.table_name_prompter(sql_connection)
            sql_func.table_creator(sql_connection, table_name, var_list, data)
            print("Successfully saved Data")
            time.sleep(0.5)

    save_location = input_func.inp_save_folder()
    if save_location is None:
        interface.quit_program()

    substituter.substitute(var_list, data, template_location, save_location)

    print("Mail Merge Completed")
    time.sleep(0.5)

    # Open Saved Files in Explorer.
    interface.open_file(save_location)
    interface.quit_program()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        # This is triggered when exit function is called in any of the functions.
        pass
    except:
        # traceback.format_exc gets the full error message.
        interface.program_error(traceback.format_exc())
