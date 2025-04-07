import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.params import Depends
from dotenv import load_dotenv
import motor.motor_asyncio
app = FastAPI()
load_dotenv()
mongo_env = os.getenv("mongo_URL")

#Continually calls the function for each get request
# Connect to Mongo Atlas
async def get_database():
    # Create a new client for each request
    client = motor.motor_asyncio.AsyncIOMotorClient(
        mongo_env,
        maxPoolSize=1,
        minPoolSize=0,
        serverSelectionTimeoutMS=5000
    )
    try:
        yield client.multimedia_db
    finally:
        client.close()  # Ensure connection is closed after request


class PlayerScore(BaseModel):
 player_name: str
 score: int

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...),db=Depends(get_database)):
 # In a real application, the file should be saved to a storage service
 content = await file.read()
 sprite_doc = {"filename": file.filename, "content": content}
 result = await db.sprites.insert_one(sprite_doc)
 return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

# Endpoint for retrieving a sprite
@app.get("/get_sprite/{filename}")
async def get_sprite(filename: str, db=Depends(get_database)):
    sprite = await db.sprites.find_one({"filename": filename})
    if sprite:
        return {"filename": sprite["filename"], "content": sprite["content"]}
    return {"message": "Sprite not found"}
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...),db=Depends(get_database)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}
# Endpoint for retrieving an audio file
@app.get("/get_audio/{filename}")
async def get_audio(filename: str,db=Depends(get_database)):
    audio = await db.audio.find_one({"filename": filename})
    if audio:
        return {"filename": audio["filename"], "content": audio["content"]}
    return {"message": "Audio file not found"}

@app.post("/player_score")
async def add_score(score: PlayerScore,db=Depends(get_database)):
 score_doc = score.dict()
 result = await db.scores.insert_one(score_doc)
 return {"message": "Score recorded", "id": str(result.inserted_id)}


# Endpoint for retrieving scores
@app.get("/player_score/{player_name}")
async def get_score(player_name: str, db=Depends(get_database)):
    scores = await db.scores.find({"player_name": player_name}).to_list(length=100)
    return {"player_name": player_name, "scores": scores}