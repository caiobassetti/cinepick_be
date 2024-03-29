# Import statements
from io import BytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from api.cine_utils.generate_poster import generate_poster
from api.cine_utils.generate_synopsis import generate_syn
from api.cine_utils.morph import image_mixer_api
from api.cine_utils.char_display import movie_to_analyse


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


@app.get("/morph")
async def morph(img_1, img_2):
    print(img_1)
    char_img = image_mixer_api(img_1, img_2)
    morphed_img = list(char_img.keys())[0]
    return morphed_img

@app.get("/display")
async def display(title):
    faces_title = movie_to_analyse(title)
    img = BytesIO(faces_title)
    return Response(content = img.getvalue(), media_type="image/png")
