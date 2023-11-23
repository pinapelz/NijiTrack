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

    def _create_server_connection(self, host_name: str, user_name: str, user_password: str) -> mysql.connector:
        connection = None
        try:
            connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password)
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection

    def get_connection(self):
        return self.connection

    def _create_database(self, cursor: str, database_name: str):
        try:
            cursor.execute(
                f"CREATE DATABASE {database_name} DEFAULT CHARACTER SET 'utf8'")
        except Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    def _load_database(self, database_name: str):
        cursor = self.connection.cursor(buffered=True)
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

    def create_table(self, name: str, column: str):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(f"CREATE TABLE {name} ({column})")
            print(f"Table {name} created successfully")
        except Error as err:
            print(err)

    def insert_row(self, name: str, column: str, data: tuple):
        cursor = self.connection.cursor(buffered=True)
        try:
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {name} ({column}) VALUES ({placeholders})"
            cursor.execute(query, data)
            self.connection.commit()
            print("Data Inserted:", data, "into", name)
        except Error as err:
            print("Error inserting data")
            print(err)


    def clear_table(self, name: str):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(f"DELETE FROM {name}")
            self.connection.commit()
            print("Table cleared successfully")
        except Error as err:
            print("Error clearing table")
            print(err)

    def reset_auto_increment(self, name: str):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(f"ALTER TABLE {name} AUTO_INCREMENT = 1")
            self.connection.commit()
            print("Table reset successfully")
        except Error as err:
            print("Error resetting table")
            print(err)

    def copy_rows_to_new_table(self, name: str, new_name: str, column: str):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(
                f"INSERT INTO {new_name} ({column}) SELECT {column} FROM {name}")
            cursor.execute(
                f"ALTER TABLE {new_name} MODIFY COLUMN id INT AUTO_INCREMENT")
            self.connection.commit()
            print("Rows copied successfully")
        except Error as err:
            print("Error copying rows")
            print(err)

    def drop_table(self, name: str):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(f"DROP TABLE {name}")
            self.connection.commit()
            print("Table dropped successfully")
        except Error as err:
            print("Error dropping table")
            print(err)
    
    def check_row_exists(self, name: str, column_name: str, value: str):
        """
        Checks if a row exists in a table
        """
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(f"SELECT * FROM {name} WHERE {column_name} = '{value}'")
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Error as err:
            print("Error checking row")
            print(err)

    def update_row(self, name: str, column_name: str, search_val: str, replace_col:str, new_value: str):
        """
        Updates a row in a table
        """
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(f"UPDATE {name} SET {replace_col} = '{new_value}' WHERE {column_name} = '{search_val}'")
            self.connection.commit()
            print("Row updated successfully")
        except Error as err:
            print("Error updating row")
            print(err)
    
    def execute_query(self, query: str, data: tuple = None):
        cursor = self.connection.cursor(buffered=True)
        if data:
            try:
                cursor.execute(query, data)
                result = cursor.fetchall()
                return result
            except Error as err:
                print("Error executing query")
                print(err)
                return None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print("Error executing query")
            print(err)
    
    def get_query_result(self, query: str):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print("Error executing query")
            print(err)
    