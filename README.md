# About

A poetry project that uses FastAPI and uvicorn to create and host an API that detects objects in an image using the real-time object detection algorithm YOLOv3.

## Getting started

### Prerequisites

You have [poetry](https://python-poetry.org/docs/) installed.

### 1. Clone the project

```bash
https://github.com/CarolBrandao/image_detection_yolov3.git
```

### 2. Install the dependencies

First, make sure you are in the root directory. If you just cloned the project you may have to run:

```bash
cd image-detection-yolov3
```

Then you can run:

```bash
poetry install
```

Done!

## How it works

There are two ways of using this project to detect images:

### 1. Run it for a batch of images at once

On the folder `images` there are a few example images. In order to run the object detection for all images on that folder, you can use:

```bash
poetry run local
```

As output you will get the same images, but with the object selected and labeled. For example:

![Example of output image](/docs_images/output_example_1.png "Example of output image").

The output images will be available at the directory `images_with_boxes` which is automatically generated when running `poetry run local`.

### 2. Use a hosted API

In case you want to go with this option, you should run:

```bash
poetry run start_server
```

This command will startup the uvicorn server on port 8000.

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and feel free to play around with the API. This is how it should look like:

![How the server hosted looks like](/docs_images/localhost_1.png "How the server hosted looks like").

Trying out the `predict` endpoint you should be possible clicking "Try out" button that lays under "/predict".

![Image showing where try out button is](/docs_images/try_out.png "Try out").

After that you should be able to select desired model (`yolo-v3` or `yolo-v3-tiny`), upload your image and click on `Execute`:

![Example of output image](/docs_images/output_example_2.png "Example of output image").
