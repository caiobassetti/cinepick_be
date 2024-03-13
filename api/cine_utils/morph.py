# Import Statements
import json
from gradio_client import Client


def image_mixer_api(path_1, path_2):
    """
    API that calls the image-mixer-demo app from HuggingFace
    """
    client = Client("https://lambdalabs-image-mixer-demo.hf.space/")

    result = client.predict(
				"Text/URL",	# str  in 'Input 0 type' Radio component
				"Text/URL",	# str  in 'Input 1 type' Radio component
				path_1,	# str  in 'Text or Image URL' Textbox component
				path_2,	# str  in 'Text or Image URL' Textbox component
				"",	# str (filepath or URL to image) in 'Image' Image component
				"",	# str (filepath or URL to image) in 'Image' Image component
				2.5,	# int | float (numeric value between 0 and 5) in 'Strength' Slider component
				2.5,	# int | float (numeric value between 0 and 5) in 'Strength' Slider component
				3,	# int | float (numeric value between 1 and 10) in 'CFG scale' Slider component
				1,	# int | float (numeric value between 1 and 1) in 'Num samples' Slider component
				0,	# int | float (numeric value between 0 and 10000) in 'Seed' Slider component
				10,	# int | float (numeric value between 10 and 100) in 'Steps' Slider component
				fn_index=2
    )

    path_to_json = result + "/captions.json"

    # Open the JSON file and read its contents
    with open(path_to_json, "r") as file:
        data = json.load(file)

    return data
