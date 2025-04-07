import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.params import Depends
from dotenv import load_dotenv
import motor.motor_asyncio

app = FastAPI()
load_dotenv()
mongo_env = os.getenv("mongo_URL")

# Connect to Mongo Atlas
async def get_database():
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


# Input validation for player scores
class PlayerScore(BaseModel):
    player_name: str
    score: int

@app.get("/")
async def root():
    return {"message": "You are connected"}

@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...), db=Depends(get_database)):
    content = await file.read()
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".gif")):  # Validate file type
        raise HTTPException(status_code=400, detail="Invalid file type")
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.get("/get_sprite/{filename}")
async def get_sprite(filename: str, db=Depends(get_database)):
    sprite = await db.sprites.find_one({"filename": filename})
    if sprite:
        return {"filename": sprite["filename"], "content": sprite["content"]}
    raise HTTPException(status_code=404, detail="Sprite not found")

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...), db=Depends(get_database)):
    content = await file.read()
    if not file.filename.endswith((".mp3", ".wav", ".aac")):  # Validate file type
        raise HTTPException(status_code=400, detail="Invalid file type")
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.get("/get_audio/{filename}")
async def get_audio(filename: str, db=Depends(get_database)):
    audio = await db.audio.find_one({"filename": filename})
    if audio:
        return {"filename": audio["filename"], "content": audio["content"]}
    raise HTTPException(status_code=404, detail="Audio file not found")

@app.post("/player_score")
async def add_score(score: PlayerScore, db=Depends(get_database)):
    score_doc = score.model_dump()  # Ensure sanitized inputs
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

@app.get("/player_score/{player_name}")
async def get_score(player_name: str, db=Depends(get_database)):
    if not player_name.isalnum():  # Validate player_name format
        raise HTTPException(status_code=400, detail="Invalid player name format")
    scores = await db.scores.find({"player_name": player_name}).to_list(length=100)
    return {"player_name": player_name, "scores": scores}