# import os
# from dotenv import load_dotenv

# load_dotenv()
# config = os.environ


# DB_USERNAME = config.get("MONGO_USERNAME", "")
# DB_PASSWORD = config.get("MONGO_PASSWORD", "")
# DB_HOST = config.get("MONGO_DB_HOST", "mongo")
# DB_PORT = config.get("MONGO_DB_PORT", 27017)
# DB_NAME = config.get("MONGO_DB_NAME", "")

# MONGO_URI = f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin&retryWrites=true&w=majority"

# config["DB_NAME"] = DB_NAME
# config["MONGO_URI"] = MONGO_URI
import os
from dotenv import load_dotenv

# load theo ENV
env = os.getenv("ENV", "dev")
load_dotenv(f".env.{env}")

config = os.environ

DB_USERNAME = config.get("MONGO_USERNAME", "")
DB_PASSWORD = config.get("MONGO_PASSWORD", "")
DB_HOST = config.get("MONGO_DB_HOST", "localhost")
DB_PORT = int(config.get("MONGO_DB_PORT", 27018))
DB_NAME = config.get("MONGO_DB_NAME", "")

MONGO_URI = f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin&retryWrites=true&w=majority"

config["MONGO_URI"] = MONGO_URI