from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["ghg-exploration"]
users_collection = db["users"]
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "332332547761-553uld75u11qih884rhfpiesj4u944is.apps.googleusercontent.com")
