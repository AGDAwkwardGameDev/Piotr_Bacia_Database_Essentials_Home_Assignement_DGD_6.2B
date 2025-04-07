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
    return {"message": "You are connected"}#Creates a message on-screen to inform the user if the site is working correctly.

@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...), db=Depends(get_database)):
    content = await file.read()
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".gif")):  #Validates if file type is an image
        raise HTTPException(status_code=400, detail="Invalid file type") #If not, sends back this message
    sprite_doc = {"filename": file.filename, "content": content} #creates the instance of the data to send
    result = await db.sprites.insert_one(sprite_doc) #injects the data into the Mongo database collection at the sprites table
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)} #returns message with the data variables

@app.get("/get_sprite/{filename}")
async def get_sprite(filename: str, db=Depends(get_database)):
    sprite = await db.sprites.find_one({"filename": filename})#calls for data that matches the filename from the Mongo Database at sprites
    if sprite:#checks if data exists
        return {"filename": sprite["filename"], "content": sprite["content"]}#returns the data from the collection
    raise HTTPException(status_code=404, detail="Sprite not found")#returns message if the data does not exist

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...), db=Depends(get_database)):
    content = await file.read()
    if not file.filename.endswith((".mp3", ".wav", ".aac")):  #Validates if file type is an audio file
        raise HTTPException(status_code=400, detail="Invalid file type") #if not, sends back this message
    audio_doc = {"filename": file.filename, "content": content} #creates an instance of the data to send
    result = await db.audio.insert_one(audio_doc) # injects the data into the Mongo database collection at the audio table
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)} #returns message with the data variables

@app.get("/get_audio/{filename}")
async def get_audio(filename: str, db=Depends(get_database)):
    audio = await db.audio.find_one({"filename": filename})#calls for data that matches the filename from the Mongo Database in audio
    if audio:#checks if the data exists
        return {"filename": audio["filename"], "content": audio["content"]}#returns the data from the collection
    raise HTTPException(status_code=404, detail="Audio file not found")#Returns a message if the data does not exist

@app.post("/player_score")
async def add_score(score: PlayerScore, db=Depends(get_database)):
    score_doc = score.model_dump()  # Ensures sanitized inputs from the user
    result = await db.scores.insert_one(score_doc) #injects the data into the Mongo collection at scores
    return {"message": "Score recorded", "id": str(result.inserted_id)} #returns message with the data variables

@app.get("/player_score/{player_name}")
async def get_score(player_name: str, db=Depends(get_database)):
    if not player_name.isalnum():  # Validate player_name format
        raise HTTPException(status_code=400, detail="Invalid player name format")#sends out the error message if player_name format isn't valid
    scores = await db.scores.find({"player_name": player_name}).to_list(length=100)# gets the data from the Mongo Database with the player_name
    return {"player_name": player_name, "scores": scores}#returns the data