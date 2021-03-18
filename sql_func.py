"""sql_func.py : Handles MySQL Database operations."""
import mysql.connector
from interface import user_error
import traceback

database_name = "MailMerge"


def sql_connect(username, password):
    """Connect to MySQL Server running in localhost"""
    try:
        sql_connection = mysql.connector.connect(host='localhost', user=username, password=password)
    except:
        user_error("SQL ERROR :\n" + traceback.format_exc())
    else:
        return sql_connection


def table_name_prompter(sql_connection):
    """Asks User for a new table name."""
    while True:
        table_name = input('Enter a Table Name:')
        cursor = sql_connection.cursor()
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()

        table_list = []
        for row in tables:
            table_list.append(row[0])

        if table_name in table_list:
            print(table_name, 'already exists. Choose Again..')
        else:
            return table_name


def table_creator(sql_connection, table_name, var_list, data):
    """Creates a new table and inserts data in it."""

    table_creator_cursor = sql_connection.cursor()

    # Generate SQL for creating table containing user's data.
    table_creator_sql = f"create table `{table_name}` ("
    for _ in var_list[:-1]:
        table_creator_sql += "`%s` longtext not null,"
    table_creator_sql += "`%s` longtext not null);"

    table_creator_cursor.execute(table_creator_sql, var_list)

    # Generate sql for inserting data into the table.
    data_inserter_sql = f"insert into {table_name} values("
    for _ in data[0]:
        data_inserter_sql += "%s,"
    data_inserter_sql = data_inserter_sql.rstrip(",") + ");"

    data_inserter_cursor = sql_connection.cursor()
    data_inserter_cursor.executemany(data_inserter_sql, data)

    sql_connection.commit()


def database_creator(sql_connection: mysql.connector.connection.MySQLConnection):
    """Creates database if it doesnt exist and uses it."""

    database_creator_cursor = sql_connection.cursor()
    database_creator_cursor.execute(f"create database if not exists `{database_name}`")

    database_user_cursor = sql_connection.cursor()
    database_user_cursor.execute(f"use `{database_name}`")


def sql_access_prompt():
    """Asks user whether to use data saved in a MySQL Table."""

    choice = input('Do you want to use data saved in a MySQL Table    (Y/N)\n>')

    if choice.lower() == 'y':
        username = input('Enter the username:')
        password = input('Enter the password:')
    else:
        return

    sql_connection = sql_connect(username, password)

    while True:
        table_name = input(f'Enter the Table Name (Must be in a database named {database_name}):')
        database_creator(sql_connection)
        table_checker_cursor = sql_connection.cursor()
        table_checker_cursor.execute('SHOW TABLES')
        tables = table_checker_cursor.fetchall()

        table_list = []
        for row in tables:
            table_list.append(row[0])

        if table_name not in table_list:
            print(table_name, 'does not exist.')
        else:
            return table_name, sql_connection


def data_getter(sql_connection: mysql.connector.MySQLConnection, table_name, var_list):
    """Gets data from the MySQL Table."""

    data_getter_cursor = sql_connection.cursor()

    # Generate SQL for getting data in alphabetical order of column headers.
    data_getter_sql = "select"
    for _ in var_list:
        data_getter_sql += "`%s`,"
    data_getter_sql = data_getter_sql.rstrip(",") + f"from `{table_name}`;"

    data_getter_cursor.execute(data_getter_sql, var_list)
    data = data_getter_cursor.fetchall()
    return data


def verify_data(sql_connection, var_list, table_name):
    """Check whether the table contains the data required."""

    cursor = sql_connection.cursor()
    cursor.execute("DESCRIBE `{}`".format(table_name))

    field_names = cursor.fetchall()

    table_headers = []
    for field in field_names:
        # Remove single quotes from field names that are added while creating tables
        # and also remove extra MySQL escape characters.
        table_headers.append(field[0].strip("\'").replace("\\", ""))

    for val in var_list:
        if val not in table_headers:
            return False
    return True
