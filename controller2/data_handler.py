from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING

uri = "mongodb+srv://test_user2:EOfApjntJgGosIJ6@smartcity.4okvjzf.mongodb.net/?retryWrites=true&w=majority&appName=SmartCity"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sensor']

def test_connection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def search_whole_table(table):
    collection = db[table]
    latest_document = list(collection.find().sort("timestamp", DESCENDING).limit(1))
    for doc in latest_document:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    return latest_document

