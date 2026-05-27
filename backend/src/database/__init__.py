import os
import motor.motor_asyncio

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_URI: mongodb://admin:admin123@mongo:27017/ecommerce?authSource=admin

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database("ecommerce")