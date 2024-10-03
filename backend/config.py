from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["ghg-exploration"]
users_collection = db["users"]