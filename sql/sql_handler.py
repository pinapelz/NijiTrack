import mysql.connector
from mysql.connector import Error, errorcode


class SQLHandler:
    def __init__(self, host_name: str, user_name: str, user_password: str, database_name: str):
        self.host_name = host_name
        self.username = user_name
        self.password = user_password
        self.database_name = database_name
        self.connection = self._create_server_connection(
            host_name, user_name, user_password)
        self._load_database(database_name)

    def _create_server_connection(self, host_name: str, user_name: str, user_password: str, exclude=None) -> mysql.connector:
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection

    def _create_database(self, cursor: str, database_name: str):
        try:
            cursor.execute(
                f"CREATE DATABASE {database_name} DEFAULT CHARACTER SET 'utf8'")
        except Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    def _load_database(self, database_name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"USE {database_name}")
            print(f"Database {database_name} loaded successfully")
        except Error as err:
            print(f"Database {database_name} does not exist")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self._create_database(cursor, database_name)
                print(f"Database {database_name} created successfully")
                self.connection.database = database_name
            else:
                print(err)
                exit(1)

    def create_table(self, table_name: str, table_columns: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CREATE TABLE {table_name} ({table_columns})")
            print(f"Table {table_name} created successfully")
        except Error as err:
            print(err)

    def insert_data(self, table_name: str, table_columns: str, data: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {table_name} ({table_columns}) VALUES ({data})")
            self.connection.commit()
            print("Data inserted successfully")
        except Error as err:
            print("Error inserting data")
            print(err)

    def clear_table(self, table_name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table_name}")
            self.connection.commit()
            print("Table cleared successfully")
        except Error as err:
            print("Error clearing table")
            print(err)

    def reset_auto_increment(self, table_name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")
            self.connection.commit()
            print("Table reset successfully")
        except Error as err:
            print("Error resetting table")
            print(err)

    def copy_rows_to_new_table(self, table_name: str, new_table_name: str, table_columns: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {new_table_name} ({table_columns}) SELECT {table_columns} FROM {table_name}")
            cursor.execute(
                f"ALTER TABLE {new_table_name} MODIFY COLUMN id INT AUTO_INCREMENT")
            self.connection.commit()
            print("Rows copied successfully")
        except Error as err:
            print("Error copying rows")
            print(err)

    def drop_table(self, table_name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"DROP TABLE {table_name}")
            self.connection.commit()
            print("Table dropped successfully")
        except Error as err:
            print("Error dropping table")
            print(err)
    
    def check_row_exists(self, table_name: str, column_name: str, value: str):
        """
        Checks if a row exists in a table
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = '{value}'")
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Error as err:
            print("Error checking row")
            print(err)

    def update_row(self, table_name: str, column_name: str, search_val: str, replace_col:str, new_value: str):
        """
        Updates a row in a table
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"UPDATE {table_name} SET {replace_col} = '{new_value}' WHERE {column_name} = '{search_val}'")
            self.connection.commit()
            print("Row updated successfully")
        except Error as err:
            print("Error updating row")
            print(err)