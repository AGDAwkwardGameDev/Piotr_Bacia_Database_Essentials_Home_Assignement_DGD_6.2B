# Multimedia Management API

This project is a FastAPI-based RESTful API for managing multimedia files (sprites and audio) and player scores. It includes endpoints for uploading, retrieving, and managing multimedia files and player scores, and uses a MongoDB database for storage.

Additionally, this project is configured to be deployed on Vercel, a platform for hosting applications, using the `vercel.json` configuration file.

---

## Features

- Upload and retrieve sprite images.
- Upload and retrieve audio files.
- Add and retrieve player scores.
- Validates file types and player name format for security.
- Deployable as a Vercel-hosted application.
---

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.10+
- MongoDB
- A suitable virtual environment tool like `venv`.

---

## Setting Up the Environment Locally

Follow these steps to set up the development environment for this project:

1. Clone the repository to your local machine.
2. Set up a Python virtual environment:
    ```bash
    python -m venv env
    ```
3. Activate the virtual environment:
    - On macOS/Linux:
        ```bash
        source env/bin/activate
        ```
    - On Windows:
        ```bash
        env\Scripts\activate
        ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Configure the `.env` file with the following content:
    ```
    mongo_URL=<your_mongodb_connection_string>
    ```
6. Run the application:
    ```bash
    uvicorn main:app --reload
    ```
7. Access the API at `http://127.0.0.1:8000/`.


---

## Endpoints

### Root
- `GET /`: Checks if the API is running successfully.

### Sprite Management
- `POST /upload_sprite`: Uploads a sprite image file.
- `GET /get_sprite/{filename}`: Retrieves a sprite by its filename.

### Audio Management
- `POST /upload_audio`: Uploads an audio file.
- `GET /get_audio/{filename}`: Retrieves audio by its filename.

### Player Scores
- `POST /player_score`: Records a player's score.
- `GET /player_score/{player_name}`: Retrieves scores for a given player.

---

## Requirements

The following dependencies are listed in the `requirements.txt` file:
annotated-types==0.7.0 anyio==4.9.0 certifi==2025.1.31 charset-normalizer==3.4.1 click==8.1.8 colorama==0.4.6 dnspython==2.7.0 fastapi==0.115.12 h11==0.14.0 idna==3.10 motor==3.7.0 pydantic==2.11.2 pydantic_core==2.33.1 pymongo==4.11.3 python-dotenv==1.1.0 python-multipart==0.0.20 requests==2.32.3 sniffio==1.3.1 starlette==0.46.1 typing-inspection==0.4.0 typing_extensions==4.13.1 urllib3==2.3.0 uvicorn==0.34.0


---

## Notes

- Ensure the MongoDB service is running before starting the application.
- Replace `<your_mongodb_connection_string>` in `.env` with your actual MongoDB connection string.
- The vercel.json file specifies the build and routing configurations necessary for deploying the project on Vercel.

---
