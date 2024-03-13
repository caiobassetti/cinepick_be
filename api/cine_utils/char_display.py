# Import statements
import cv2
import dlib
from google.cloud import storage
import io
import face_recognition
import numpy as np
import os
import pickle
from PIL import Image
from sklearn.cluster import DBSCAN
import random
import pandas as pd
from collections import Counter


def movie_to_analyse(title):

    table_path = os.getenv("CINE_PICK_TABLE")
    df = pd.read_csv(table_path)

    # Get the path to the key file from the environment variable
    key_file_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Authenticate with Google Cloud using the key file
    client = storage.Client.from_service_account_json(key_file_path)

    bucket_name = "cine_ethics"
    bucket = client.get_bucket(bucket_name)

    movie_info = df[df["title"] == title.lower()]

    # Path to the movie on the bucket
    movie_path = movie_info["paths"]

    # Store the image path names
    faces_list_paths = []

    # Load the pre-trained face detector model from Dlib
    detector = dlib.get_frontal_face_detector()

    faces_list = [] # List to store the images that have faces
    data = [] # List to store the encodings

    # Get blobs within the movie folder
    blobs = bucket.list_blobs(prefix=movie_path)

    # Get a random sample of blobs
    sample_size = 300 # Number of images to sample as opposed to the full 1k
    random_sample = random.sample(list(blobs), sample_size)

    for blob in random_sample:
        # Download the image as bytes
        img_bytes = blob.download_as_bytes()

        # Open the image
        img = Image.open(io.BytesIO(img_bytes))

        # Convert image to an array
        img = np.array(img)

        # Convert image to grayscale (required for Haar cascades)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = detector(gray)

        # If image is detected as a face
        if len(faces) > 0:

            # Append the image with detected faces
            faces_list.append(img)

            # Append image path
            faces_list_paths.append(blob.name)

            # Convert image to colour scale
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model="hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # build a dictionary of the image path, bounding box location,
            # and facial encodings for the current image
            d = [{"imagePath": blob.name, "loc": box, "encoding": enc}
                for (box, enc) in zip(boxes, encodings)]
            data.extend(d)

    # Write the encodings to disk
    path_encodings = os.path.join("raw_data/deep_face_encodings/", movie_info["title"].values[0])
    path_encodings = str(path_encodings)

    # Ensure that the directory exists
    os.makedirs(str(path_encodings), exist_ok=True)

    # Dump the facial encodings data to disk
    file_name = movie_info["title"].values[0] + ".pickle"
    file_name = str(file_name)

    f = open(os.path.join(path_encodings, file_name), "wb")
    f.write(pickle.dumps(data))
    f.close()

    # Load the serialized face encodings + bounding box locations from
    # disk, then extract the set of encodings to so we can cluster on them
    encodings_path = os.path.join(path_encodings, file_name)

    data = pickle.loads(open(encodings_path, "rb").read())
    data = np.array(data)

    encodings = [d["encoding"] for d in data]

    # Fitting model
    clt = DBSCAN(metric="euclidean", n_jobs=-1)
    clt.fit(encodings)

    # get the most frequent face
    count = Counter(clt.labels_)
    most = max(count, key=count.get)

    # Find all indexes into the `data` array that belong to the
    # current label ID, then get the last image
    idxs = np.where(clt.labels_ == most)[0]
    idxs = idxs[-1]

    # Load the input image from Google Cloud Storage and extract the face ROI
    blob = client.bucket(bucket_name).blob(data[idxs]["imagePath"])
    image_bytes = blob.download_as_string()

    return image_bytes
