# Import statements
from io import BytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from api.cine_utils.generate_poster import generate_poster
from api.cine_utils.generate_synopsis import generate_syn


app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/poster")
async def poster(title_1, title_2):
    new_image = generate_poster(title_1, title_2)
    img = BytesIO(new_image)
    return Response(content = img.getvalue(), media_type="image/png")


@app.get("/synopsis")
async def synopsis(title_1, title_2):
    syn = generate_syn(title_1, title_2)
    return syn
