import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
mongoClient = MongoClient(DATABASE_URL)
db = mongoClient["wcdatabase"]

