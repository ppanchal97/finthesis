from dotenv import load_dotenv
load_dotenv()

import os
import logging
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket
from query_service import QueryService
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI
from schemas import QueryParameterizationData, QueryExecutionData


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
openai_client = None
mongo_client: AsyncIOMotorClient = None
mongo_db = None
service = None 

API_BASE_PATH = f"/{os.environ.get('API_ENVIRONMENT')}/api/v{os.environ.get('API_VERSION')}"
print(API_BASE_PATH)

# clients
openai_client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'))

# MongoDB connection
mongo_client: AsyncIOMotorClient = None
mongo_db = None


async def startup_db_client():
    global mongo_client, mongo_db, service
    mongo_uri = os.environ.get('MONGODB_URI')
    mongo_client = AsyncIOMotorClient(mongo_uri)
    mongo_db = mongo_client[os.environ.get('MONGODB_DATABASE_NAME')]
    service = QueryService(openai_client=openai_client, db_client=mongo_db)
    print(f"Established Connection to DB {os.environ.get('MONGODB_DATABASE_NAME')}")

async def shutdown_db_client():
    try:
        mongo_client.close()
        print("MongoDB connection closed")
    except Exception as e:
        logging.error(f"Failed to close MongoDB connection: {str(e)}")

app.router.add_event_handler("startup", startup_db_client)
app.router.add_event_handler("shutdown", shutdown_db_client)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(f"{API_BASE_PATH}/query/parameterize")
async def parameterize_query(data: QueryParameterizationData):
    print(f"Parameterizing query: {data.query} ⏳")
    if not data.query:
        raise HTTPException(status_code=400, detail="No query provided")
    try:
        parameterized_query = await service.parameterize_query(data.query)
        return parameterized_query
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post(f"{API_BASE_PATH}/query/execute")
async def execute_query(data: QueryExecutionData):
    print(f"Executing query: {data.query} ⏳")
    if not data.query:
        raise HTTPException(status_code=400, detail="No query provided")
    try:
        execution_result = await service.execute_query(data)
        return execution_result
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.websocket(f"{API_BASE_PATH}/news-feed")
async def news_feed(websocket: WebSocket):
    from news_feed import news_feed
    await websocket.accept()
    try:
        while True:
            data = "News update from the server"
            await websocket.send_text(data)
            # You could also listen for messages from the client
            # data_from_client = await websocket.receive_text()
            await asyncio.sleep(7)
            # Send the first 2 news items immediately
            await websocket.send_json(news_feed[0:2])

            # Send subsequent news items every 7 seconds
            for news in news_feed[1:]:
                await asyncio.sleep(7)  # Wait for 7 seconds
                await websocket.send_json(news)

    except Exception as e:
        logging.error(f"WebSocket connection error: {str(e)}")
    finally:
        await websocket.close()