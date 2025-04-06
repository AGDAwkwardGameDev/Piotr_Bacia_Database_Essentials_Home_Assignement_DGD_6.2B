from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio
app = FastAPI()
# Connect to Mongo Atlas

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://admin:mcast234@de-cluster.mefrd.mongodb.net/?retryWrites=true&w=majority&appName=DE-Cluster")
db = client.multimedia_db
class PlayerScore(BaseModel):
 player_name: str
 score: int
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
 # In a real application, the file should be saved to a storage service
 content = await file.read()
 sprite_doc = {"filename": file.filename, "content": content}
 result = await db.sprites.insert_one(sprite_doc)
 return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

# Endpoint for retrieving a sprite
@app.get("/get_sprite/{filename}")
async def get_sprite(filename: str):
    sprite = await db.sprites.find_one({"filename": filename})
    if sprite:
        return {"filename": sprite["filename"], "content": sprite["content"]}
    return {"message": "Sprite not found"}
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}
# Endpoint for retrieving an audio file
@app.get("/get_audio/{filename}")
async def get_audio(filename: str):
    audio = await db.audio.find_one({"filename": filename})
    if audio:
        return {"filename": audio["filename"], "content": audio["content"]}
    return {"message": "Audio file not found"}

@app.post("/player_score")
async def add_score(score: PlayerScore):
 score_doc = score.dict()
 result = await db.scores.insert_one(score_doc)
 return {"message": "Score recorded", "id": str(result.inserted_id)}


# Endpoint for retrieving scores
@app.get("/player_score/{player_name}")
async def get_score(player_name: str):
    scores = await db.scores.find({"player_name": player_name}).to_list(length=100)
    return {"player_name": player_name, "scores": scores}