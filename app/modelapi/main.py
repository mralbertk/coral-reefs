import os
import time
import uuid

import cv2
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile

import config as cfg

# FastAPI instance
app = FastAPI()


@app.get("/")
def read_root():
    """Sign of life to confirm API is active"""
    return {"message": "API is alive"}


@app.get("/models")
async def get_models():
    """Return the collection of available models"""
    return {"models": sorted(cfg.models)}


# Get an image from the frontend and apply selected model
@app.post("/files/{model}")
async def get_file(model: str = None, file: UploadFile = File(...)):
    """
    Receives a file as bytes object via POST.
    Processes the image with OpenCV and saves
    it to the storage location. Returns the
    location of the processed image.
    """
    start = time.time()
    image = np.array(Image.open(file.file))

    # Read image with OpenCV as RGB (instead of BGR)
    img = cv2.cvtColor(image, cv2.cv2.COLOR_RGB2BGR)

    # Output name
    if not model:
        name = f'{cfg.paths["export"]}{uuid.uuid4()}.jpg'
    else:
        name = f'{cfg.paths["export"]}{uuid.uuid4()}_{model}.jpg'

    # Apply the selected model
    output = cfg.models[model](img)

    # Write output to storage
    cv2.imwrite(name, output)

    # Time tracking
    end = time.time()
    elapsed = end - start

    # Return location of new image
    return {"time": elapsed,
            "output": name}


# Get an image from the frontend and generate preview thumbnails
@app.post("/preview")
async def generate_preview(file: UploadFile = File(...)):
    """
    Receives an image via POST and applies
    all filters stored in the config file
    to a 256x256 downsized version of the
    image. Saves all images to /preview
    directory and returns the locations of
    all images as list.
    """
    thumbnails = []
    start = time.time()
    image = np.array(Image.open(file.file))

    img = cv2.cvtColor(image, cv2.cv2.COLOR_RGB2BGR)
    res = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)

    for model in cfg.models:
        name = f'{cfg.paths["preview"]}{uuid.uuid4()}_{model}.jpg'
        output = cfg.models[model](res)
        cv2.imwrite(name, output)
        thumbnails.append((model, name))

    end = time.time()
    elapsed = end - start

    return {"time": elapsed,
            "thumbs": thumbnails}


# Delete files from backend file system when they are no longer needed
@app.post("/cleanup/{folder}")
async def cleanup(folder: str):
    """
    Temporary implementation. Deletes all files in
    the /preview folder whenever an actual image
    export is created.
    """
    # Track number of deleted files
    removed = 0

    start = time.time()

    # Get all files in directory
    match folder:

        case "preview":
            dst = cfg.paths["preview"]

        case "export":
            dst = cfg.paths["export"]

    files = os.listdir(dst)

    # Remove files
    for file in files:
        os.remove(f"{dst}/{file}")
        removed += 1

    end = time.time()
    elapsed = end - start

    # Return
    return {"time": elapsed,
            "removed": removed}
