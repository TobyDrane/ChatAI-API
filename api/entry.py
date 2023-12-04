import os

from contextlib import asynccontextmanager
import pymongo

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.controller.conversation import conversation_router

try:
    load_dotenv()
except OSError:
    pass

origins = ["http://localhost"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establish connection to database
    app.mongodb_client = pymongo.MongoClient(
        os.environ.get("MONGO_URI"), uuidRepresentation="standard"
    )
    app.database = app.mongodb_client[os.environ.get("DB")]

    yield

    # Perform any other required cleanup here
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router)


@app.get("/")
def ping():
    return {"message": "pong"}
