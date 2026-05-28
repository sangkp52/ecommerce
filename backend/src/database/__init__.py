import os
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database("ecommerce")