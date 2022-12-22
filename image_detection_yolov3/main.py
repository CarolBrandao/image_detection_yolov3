from .helpers import detect_and_draw_box, create_dir
from .model import Model
import io
import os
import cv2
import cvlib as cv
import uvicorn
import numpy as np
import nest_asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from cvlib.object_detection import draw_bbox

# Some example images
image_files = [
    'apple.png',
]

def local():
    # Runs the image detection for the images salved in the images directory.
    # The output will be saved on the "images_with_boxes" directory.
    create_dir("images_with_boxes")

    for image_file in image_files:
        detect_and_draw_box(image_file)

def start_server():
    create_dir("images_uploaded")

    app = FastAPI()

    app = FastAPI(title='Deploying a ML Model with FastAPI')

    # By using @app.get("/") you are allowing the GET method to work for the / endpoint.
    @app.get("/")
    def home():
        return "Congratulations! Your API is working as expected. Now head over to http://localhost:8000/docs."

    # This endpoint handles all the logic necessary for the object detection to work.
    # It requires the desired model and the image in which to perform object detection.
    @app.post("/predict")
    def prediction(model: Model, file: UploadFile = File(...)):

        # 1. VALIDATE INPUT FILE
        filename = file.filename
        fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
        if not fileExtension:
            raise HTTPException(status_code=415, detail="Unsupported file provided.")

        # 2. TRANSFORM RAW IMAGE INTO CV2 image

        # Read image as a stream of bytes
        image_stream = io.BytesIO(file.file.read())

        # Start the stream from the beginning (position zero)
        image_stream.seek(0)

        # Write the stream of bytes into a numpy array
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)

        # Decode the numpy array as an image
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)


        # 3. RUN OBJECT DETECTION MODEL

        # Run object detection
        bbox, label, conf = cv.detect_common_objects(image, model=model)

        # Create image that includes bounding boxes and labels
        output_image = draw_bbox(image, bbox, label, conf)

        # Save it in a folder within the server
        cv2.imwrite(f'images_uploaded/{filename}', output_image)


        # 4. STREAM THE RESPONSE BACK TO THE CLIENT

        # Open the saved image for reading in binary mode
        file_image = open(f'images_uploaded/{filename}', mode="rb")

        # Return the image as a stream specifying media type
        return StreamingResponse(file_image, media_type="image/jpeg")

    # Allows the server to be run in this interactive environment
    nest_asyncio.apply()

    # Host depends on the setup you selected (docker or virtual env)
    host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"

    # Spin up the server!
    uvicorn.run(app, host=host, port=8000)