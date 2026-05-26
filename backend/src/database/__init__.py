# import motor.motor_asyncio
# from config import config


# client = motor.motor_asyncio.AsyncIOMotorClient(config.get("MONGO_URI"))
# db = client[config["DB_NAME"]]
import os
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database("ecommerce")