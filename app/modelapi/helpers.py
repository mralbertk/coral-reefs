import numpy as np
import cv2
from PIL import Image

from models.reframing.custom_config import custom_config
from models.reframing.warping import warping
from models.reframing.contour import *
from models.reframing.intersection import *
from fastapi import File, UploadFile


def param_types(params: dict) -> dict:
    """
    Converts dictionary values of parameters to the
    correct data types for filters to process.
    """
    for param in params:
        match param:
            case "omega" | "t0" | "percent":
                params[param] = float(params[param])
            case "blockSize":
                params[param] = int(params[param])
            case "meanMode":
                params[param] = bool(params[param])
    return params


def main_reframing(model_path: str, img: UploadFile = File(...), newSize: int = 400) -> object:
    """
    Detects square frames in images. Rotates the frame so that
    it is straight in the frame. Crops the image to the frame
    border.
    """
    # load predictor from model
    predictor = custom_config(model_path=model_path)

    # read image
    image = np.array(Image.open(file.file))

    # Read image with OpenCV as RGB (instead of BGR)
    img = cv2.cvtColor(image, cv2.cv2.COLOR_RGB2BGR)

    # Not sure what this does - Noah!?
    rows, cols = img.shape[:2]

    # prediction
    output = predictor(img)

    # get mask
    mask_array = 1 * output["instances"].get('pred_masks').to('cpu').numpy()
    mask_array = np.moveaxis(mask_array, 0, -1)
    mask_array = np.repeat(mask_array, 3, axis=2)
    output = np.where(mask_array == False, 0,
                      (np.where(mask_array == True, 255, img)))

    mask3d = output
    mask = mask3d[:, :, 1]

    # Find contour of the mask
    cnts = find_contour(mask)

    # Fist step : First corners estimations
    screenCnt = minimum_area_enclosing(cnts)

    # Second step: Fit 4 lines on each edges
    lines_pts = fit_lines_on_edges(cnts, screenCnt, rows, cols)

    # Third step: Lines intersection to get corners
    newCnt = get_lines_intersections(lines_pts, ncols=cols, nrows=rows)

    # Last step: Reframing
    warped = warping(img, pts=np.float32(newCnt[:, 0]), newSize=newSize)

    return warped
