"""
MongoDB
"""
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

mongo_url = config("MONGODB_URL")
mongo_max_connections = 10
mongo_min_connections = 10
mongo_db = "SFJ-MSR"
mongo_url = f"mongodb://localhost:27017/{mongo_db}"

# Sendgrid configuration


class Database:
    client: AsyncIOMotorClient = None


db = Database()



async def get_database() -> AsyncIOMotorClient:
    return db.client.sfgmsr


async def connect():
    """Connect to MONGO DB
    """
    db.client = AsyncIOMotorClient(str(mongo_url),
                                   maxPoolSize=mongo_max_connections,
                                   minPoolSize=mongo_min_connections)
                                   
    print(f"Connected to mongo at {mongo_url}")


async def close():
    """Close MongoDB Connection
    """
    db.client.close()
    print("Closed connection with MongoDB")
