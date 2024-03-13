from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import time
from functools import wraps

path_to_certificate="zertifikate/mongodb.pem"

uri = "mongodb+srv://smartcity.4okvjzf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=SmartCity"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate,
                     server_api=ServerApi('1'))
db = client['testDB']

def time_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Use await here if func is async
        end_time = time.time()
        duration = end_time - start_time
        return result, duration
    return wrapper


def test_connection():
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB connection is successful.")
    except ConnectionFailure:
        print("Server not available")

@time_query
def search_whole_table(table):
    collection = db[table]
    matching_documents = list(collection.find())
    return matching_documents

