from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import MongoClient
from dotenv import dotenv_values
from routes import router
from urllib.parse import quote_plus


config = dotenv_values("credentialS.env")
username = quote_plus(config['USERNAME'])
password = quote_plus(config['PASSWORD'])


async def connectToDatabase():
    db = MongoClient(f'mongodb+srv://{username}:{password}@udemycluster.bb3gw.mongodb.net/?retryWrites=true&w=majority&appName=UdemyCluster')
    print(db)
    return db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup has began!!")
    dbHost = await connectToDatabase()
    app.players = dbHost.tournament.players
    yield
    print("shutdown has begun!!")
    
app = FastAPI(lifespan=lifespan)
app.include_router(router)