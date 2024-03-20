import psycopg2
from psycopg2 import Error

class PostgresHandler:
    def __init__(self, username: str, password: str, host_name: str, port: int, database: str):
        db_params = {
            "dbname": database,
            "user": username,
            "password": password,
            "host": host_name,
            "port": port
        }
        self._connection = psycopg2.connect(**db_params)
        print("Handler Success")
    
    def get_connection(self):
        return self._connection

    def create_table(self, name: str, column: str):
        cursor = self._connection.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS "{name}" ({column})')
        self._connection.commit()
        cursor.close()
    
    def clear_table(self, name: str):
        cursor = self._connection.cursor()
        cursor.execute(f"DELETE FROM {name}")
        self._connection.commit()
        cursor.close()

    def check_row_exists(self, table_name: str, column_name: str, value: str):
        cursor = self._connection.cursor()
        query = f'SELECT 1 FROM "{table_name}" WHERE {column_name} = %s'
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        cursor.close()

        if result is not None:
            return True
        else:
            return False
    
    def insert_row(self, table_name, column, data):
        try:
            cursor  = self._connection.cursor()
            placeholders = ', '.join(['%s'] * len(data))
            query = f'INSERT INTO "{table_name}" ({column}) VALUES ({placeholders})'
            cursor.execute(query, data)
            self._connection.commit()
            print("Data Inserted:", data)
        except Error as err:
            self._connection.rollback()
            print("Error inserting data")
            print(err)
            if "duplicate key" not in str(err).lower():
                return False
        return True

    def update_row(self, table_name: str, column: str, value: str, update_column: str, update_value: str):
        try:
            cursor = self._connection.cursor()
            query = f'UPDATE "{table_name}" SET {update_column} = %s WHERE {column} = %s'
            cursor.execute(query, (update_value, value))
            self._connection.commit()
            print("Data Updated:", value, update_value)
        except Error as e:
            self._connection.rollback()
            print(f"Failed to update row from {table_name} WHERE {column} is {value}")
            print(e)
            return False
        return True
    
    def get_rows(self, table_name: str, column: str, value: str):
        try:
            cursor = self._connection.cursor()
            query = f'SELECT * FROM "{table_name}" WHERE {column} = %s'
            cursor.execute(query, (value,))
            result = cursor.fetchall()
            return result
        except Error as e:
            self._connection.rollback()
            print(f"Failed to fetch row from {table_name} WHERE {column} is {value}")
            print(e)
            return False
    
    def get_random_row(self, table_name: str, count: int, condition: str = None):
        if condition is None:
            condition = "1 = 1"
        try:
            cursor = self._connection.cursor()
            query = f"SELECT * FROM {table_name} WHERE {condition} ORDER BY RANDOM() LIMIT {str(count)}"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            self._connection.rollback()
            print(f"Failed to select random rows from {table_name}")
            print(e)
            return False
    
    def check_health(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            return True
        else:
            return False
    
    def delete_row(self, table_name: str, column: str, value: str):
        try:
            cursor = self._connection.cursor()
            query = f"DELETE FROM {table_name} WHERE {column} = %s"
            cursor.execute(query, (value,))
            self._connection.commit()
            print("Data Deleted:", value)
        except Error as e:
            self._connection.rollback()
            print(f"Failed to delete row from {table_name} WHERE {column} is {value}")
            print(e)
            return False
        return True
    
    def execute_query(self, query: str, data: tuple = None):
        try:
            cursor = self._connection.cursor()
            if data is None:
                cursor.execute(query)
            else:
                cursor.execute(query, data)
            result = cursor.fetchall()
            return result
        except Error as e:
            self._connection.rollback()
            print(f"Failed to execute query: {query}")
            print(e)
            return False
    
    def reset_auto_increment(self, table_name: str):
        try:
            cursor = self._connection.cursor()
            query = f"ALTER SEQUENCE {table_name}_id RESTART WITH 1"
            cursor.execute(query)
            self._connection.commit()
            print("Auto Increment Reset")
        except Error as e:
            self._connection.rollback()
            print(f"Failed to reset auto increment for {table_name}")
            print(e)
            return False
        return True
    
    def get_most_recently_added_row_time(self, table_name: str):
        try:
            cursor = self._connection.cursor()
            query = f"SELECT timestamp FROM {table_name} ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            self._connection.rollback()
            print(f"Failed to get most recently added row from {table_name}")
            print(e)
            return False

    
    def close_connection(self):
        self._connection.close()