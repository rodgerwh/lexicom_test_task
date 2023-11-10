from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import aioredis

app = FastAPI(
    title="Lexicom Test Assignment",
    description="A simple phonebook implementation",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
)

tags_metadata = [
    {"name": "get", "description": "GET requests"},
    {"name": "post", "description": "POST requests"},
]


# Define BaseModel for data
class Data(BaseModel):
    phone: str
    address: str


# Define BaseModel for responses
class MessageResponse(BaseModel):
    message: str


# Connect to Redis
async def get_redis():
    redis = await aioredis.from_url(
        "redis://lexicom_redis:6379", encoding="utf-8", decode_responses=True
    )
    return redis


# Endpoint to check data
@app.get("/check_data", response_model=Data, tags=["get"])
async def check_data(phone: str, redis=Depends(get_redis)) -> Data:
    address = await redis.get(phone)
    if not address:
        raise HTTPException(status_code=404, detail="Data not found")
    return Data(phone=phone, address=address)


# Endpoint to write or update data
@app.post("/write_data", response_model=MessageResponse, tags=["post"])
async def write_data(data: Data, redis=Depends(get_redis)) -> MessageResponse:
    await redis.set(data.phone, data.address)
    return MessageResponse(message="Data written successfully")
