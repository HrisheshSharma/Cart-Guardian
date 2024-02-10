from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bson

uri = "mongodb+srv://admin:admin@cluster0.fzklk3l.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# if "reports" in client.list_database_names():
#     print("The database exists.")
# else:
#     client.create_database("reports")
mydb = client["reports"]
report_collection = mydb["report"]

report_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["websiteURL", "status"],
        "properties": {
            "websiteURL": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "patternType": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "status": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "pattern": {
                "bsonType": "string",
                "description": "must be a string"
            },
        }
    }
}
# mydb.command("collMod", "report", validator=report_validator)

def insert_report(websiteURL, patternType, status, pattern=None):
    report = {
        "websiteURL": websiteURL,
        "patternType": patternType,
        "status": status
    }
    if pattern is not None:
        report["pattern"] = pattern
    report_collection.insert_one(report)