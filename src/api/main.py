"""
    Server application where some endpoints will be defined 
    to receive the music and classify it using the previously 
    trained ML model.
"""

import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# API service
app = FastAPI()

# CORS configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

@app.post("/{model}")
async def classify_musical_genre(model:str, file: UploadFile):
    """Controller where the music will be received and classified according to genre."""
    
    try:
        # create an .mp3 file with the received song
        contents = await file.read()
        async with aiofiles.open(file.filename, 'wb') as f:
            await f.write(contents)

    except Exception:
        return { "message": "There was an error uploading the file" }

    finally:
        await file.close()

    return { "genre": "Classic" }
