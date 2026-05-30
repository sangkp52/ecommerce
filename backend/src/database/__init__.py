from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = None
db = None

def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["ecommerce"]

def close_db():
    global client
    if client:
        client.close()

def get_db():
    return db