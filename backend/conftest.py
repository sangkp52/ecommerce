import os
from dotenv import load_dotenv

load_dotenv(".env.test")

os.environ.setdefault(
    "MONGO_URI",
    "mongodb://localhost:27018/ecommerce"
)