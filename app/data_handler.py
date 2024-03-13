from pymongo import MongoClient
from pymongo.server_api import ServerApi
import time

path_to_certificate="zertifikate/mongodb.pem"

uri = "mongodb+srv://smartcity.4okvjzf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=SmartCity"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate,
                     server_api=ServerApi('1'))
db = client['testDB']
collection = db['testCol']

def search_whole_table():
    start_time = time.time()
    result = list(collection.find())
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

if __name__ == "__main__":
    search_whole_table()
