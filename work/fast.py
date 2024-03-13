# Import statements
from io import BytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response


from api.cine_utils.generate_poster import generate_poster
from api.cine_utils.generate_synopsis import generate_syn
from api.cine_utils.morph import image_mixer_api
# from api.cine_utils.char_display import movie_to_analyse

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
async def morph(path_1, path_2, path_3, path_4):
    char_img = image_mixer_api(path_1, path_2, path_3, path_4)
    morphed_img = list(char_img.keys())[0]
    return morphed_img


# @app.get("/display")
# async def display(title):
#     faces_dict = {}
#     imread_dict = {}
#     faces_title, imread_faces_title = movie_to_analyse(title)
#     for i in range(len(faces_title)):
#         cv2.imwrite("rand_np_array.png", imread_faces_title[i])
#         faces_dict[i] = faces_title[i]
#         imread_dict[i] = imread_faces_title[i]
#     result = {"faces_title": faces_dict, "imread_faces_title": imread_dict}
#     print(result)
#     return result
