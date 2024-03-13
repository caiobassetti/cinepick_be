# Import statements
import os
import openai
import base64


def generate_poster(title_1, title_2):

    # Load environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')

    openai.api_key = openai_api_key

    # Call OpenAI API for DALL-E 2 Text to image
    prompt_image = f"movie poster mixing {title_1} and {title_2}"
    response_dalle = openai.Image.create(
                                        model="dall-e-2",
                                        prompt=prompt_image,
                                        size="1024x1024",
                                        quality="standard",
                                        response_format= "b64_json",
                                        n=1,
                                        )

    firstImage = response_dalle.data[0]
    imgData = base64.b64decode(firstImage.b64_json)

    return imgData
