from pymongo import MongoClient
##Local DB

#db_client = MongoClient().local

## Remote DB

db_client = MongoClient("mongodb+srv://test:test@cluster0.bxd4azo.mongodb.net/?retryWrites=true&w=majority").test