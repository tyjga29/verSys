import pyrqlite.dbapi2 as dbapi2
import time

database_name="foo"

# Connect to the database
connection = dbapi2.connect(
    host='localhost',
    port=4001,
)

cursor = connection.cursor()

def search_whole_table():
    query = f"SELECT * FROM {database_name}"
    result, elapsed_time = execute_query(query)
    return result, elapsed_time

def execute_query(query):
    start_time = time.time()
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(result)
    return result, elapsed_time

if __name__ == "__main__":
    search_whole_table()