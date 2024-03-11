import requests
import time
import sys

# Define the rqlite server information
RQLITE_HOST = 'localhost'
RQLITE_PORT = 4001

# Define the database name
DATABASE_NAME = 'your_database'

# Construct the rqlite API endpoint
API_ENDPOINT = f'http://{RQLITE_HOST}:{RQLITE_PORT}/db/{DATABASE_NAME}/query'

def execute_query(query):
    """
    Execute an SQL query on the rqlite database.
    
    Parameters:
        query (str): SQL query to be executed.
    
    Returns:
        dict: JSON response from the rqlite API.
    """
    payload = {'q': query}
    
    try:
        start_time = time.time()
        response = requests.post(API_ENDPOINT, json=payload)
        end_time = time.time()

        response.raise_for_status()  # Raise an exception for HTTP errors

        elapsed_time = end_time - start_time
        print(f"Query execution time: {elapsed_time:.3f} seconds")

        if elapsed_time > 2.0:
            print("Warning: Query execution may take a bit longer.")

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error executing query: {e}")
        return None

def search_whole_database():
    query = 'SELECT * FROM your_table'
    return execute_query(query)

def search_specific_column(column_name):
    query = f'SELECT {column_name} FROM your_table'
    return execute_query(query)

def find_name(name):
    query = f'SELECT * FROM your_table WHERE name = "{name}"'
    return execute_query(query)

def list_tables_and_columns():
    query = 'SHOW TABLES'
    result = execute_query(query)
    if result and 'results' in result and 'error' not in result:
        tables = result['results'][0]['values']
        for table in tables:
            print(f"Table: {table[0]}")
            columns_query = f'SHOW COLUMNS FROM {table[0]}'
            columns_result = execute_query(columns_query)
            if columns_result and 'results' in columns_result and 'error' not in columns_result:
                columns = columns_result['results'][0]['values']
                print(f"Columns: {', '.join(col[0] for col in columns)}")
            print("-" * 40)
    elif 'error' in result:
        print(f"Error in query execution: {result['error']}")
    else:
        print("Unexpected response format.")

# Run with parameter test to automatically search the whole database
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Run option 1 (Search through the whole database) automatically for testing
        result = search_whole_database(test=True)
    else:
        while True:
            print("\nMenu:")
            print("1. Search through the whole database")
            print("2. Search a specific column")
            print("3. Find a name")
            print("4. List all tables and columns")
            print("5. Write your own SQL query")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                result = search_whole_database()
            elif choice == '2':
                column_name = input("Enter the column name: ")
                result = search_specific_column(column_name)
            elif choice == '3':
                name = input("Enter the name to search: ")
                result = find_name(name)
            elif choice == '4':
                list_tables_and_columns()
                continue
            elif choice == '5':
                user_query = input("Enter your SQL query: ")
                result = execute_query(user_query)
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
                continue

            # Process the result
            if result:
                if 'results' in result and 'error' not in result:
                    rows = result['results'][0]['values']
                    for row in rows:
                        print(row)
                elif 'error' in result:
                    print(f"Error in query execution: {result['error']}")
                else:
                    print("Unexpected response format.")