import os
import time
import uuid

import cv2
import numpy as np
from enum import Enum
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Request
from helpers import param_types

import config as cfg


# FastAPI instance
app = FastAPI()


@app.get("/")
def read_root():
    """API Health Check"""
    return {"message": "OK"}


@app.get("/models")
async def get_models():
    """Return the collection of available models"""
    return {"models": sorted(cfg.models)}


@app.get("/{model}/params")
async def get_params(model: str = None) -> dict:
    """Returns the parameters for a chosen model"""
    return {"params": cfg.models[model]["params"]}


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
    output = cfg.models[model]["func"](img)

    # Write output to storage
    cv2.imwrite(name, output)

    # Time tracking
    end = time.time()
    elapsed = end - start

    # Return location of new image
    return {"time": elapsed,
            "output": name}


# Get an image from the frontend and generate preview thumbnails
@app.post("/previews")
async def generate_previews(file: UploadFile = File(...)):
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
        output = cfg.models[model]["func"](res)
        cv2.imwrite(name, output)
        thumbnails.append((model, name))

    end = time.time()
    elapsed = end - start

    return {"time": elapsed,
            "thumbs": thumbnails}


# Create a single preview image
@app.post("/preview/{model}")
async def generate_preview(model: str,
                           params: Request,
                           file: UploadFile = File(...)):
    """
    Generates a single preview image based on user-defined
    parameters.
    """
    start = time.time()
    image = np.array(Image.open(file.file))

    # Parameter type conversion
    params = dict(params.query_params)
    params = param_types(params)

    img = cv2.cvtColor(image, cv2.cv2.COLOR_RGB2BGR)
    res = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)

    name = f'{cfg.paths["preview"]}/{uuid.uuid4()}_{model}.jpg'
    output = cfg.models[model]["func"](res, **params)
    cv2.imwrite(name, output)

    end = time.time()
    elapsed = end - start

    return {"time": elapsed,
            "prev": name}


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
