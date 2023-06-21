"""
    Server application where some endpoints will be defined 
    to receive the music and classify it using the previously 
    trained ML model.
"""

import os
import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# # if the project is not being run by docker-compose, make sure 
# # you have a directory named 'api'
# if len([f for f in os.listdir() if f == 'api']) == 0:
#     os.mkdir('api')
# os.chdir('api')

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

@app.post("/")
async def classify_musical_genre(file: UploadFile):
    """Controller where the music will be received and classified according to genre."""
    try:
        contents = await file.read()
        
        print('???')
        with open('hello.txt', 'w') as s:
            s.write('hello world!')

        print(os.getcwd())
        async with aiofiles.open(file.filename, 'wb') as f:
            print('fjaskldjfals')
            await f.write(contents)
    except Exception:
        print('noooooooooooo')
        return { "message": "There was an error uploading the file" }
    finally:
        await file.close()

    return { "genre": "Classic" }
