"""
    Server application where some endpoints will be defined 
    to receive the music and classify it using the previously 
    trained ML model.
"""

import aiofiles
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

@app.post("/")
async def classify_musical_genre(
    file: Annotated[UploadFile, File(default=None)],
):
    try:
        contents = await file.read()
        async with aiofiles.open(file.filename, 'wb') as f:
            await f.write(contents)
    except Exception:
        return { "message": "There was an error uploading the file" }
    finally:
        await file.close()

    return { "genre": "Classic" }
