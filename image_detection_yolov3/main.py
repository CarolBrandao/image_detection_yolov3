from .helpers import detect_and_draw_box, create_dir
import os
import uvicorn
import nest_asyncio
from fastapi import FastAPI
from .endpoints import router

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

    # Instantiate FastAPI and include router
    app = FastAPI(title='Deploying a ML Model with FastAPI')
    app.include_router(router)

    # Allows the server to be run in this interactive environment
    nest_asyncio.apply()

    # Host depends on the setup you selected (docker or virtual env)
    host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"

    # Spin up the server!
    uvicorn.run(app, host=host, port=8000)