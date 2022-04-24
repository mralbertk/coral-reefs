from helpers.custom_config import custom_config
from helpers.warping import warping
from helpers.contour import *
from helpers.intersection import *

import boto3
import cv2
import urllib.parse
import numpy as np
from PIL import Image


def handler(event, context):
    """TODO: Add docstring"""

    # Internal storage configuration
    image_path = "/tmp/image.jpg"
    output_path = "/tmp/output.jpg"
    m_path = "/tmp/model.pth"

    # Connect to S3 & configure
    s3_client = boto3.client("s3")
    s3_image_output = "my_reframed_test.jpg"  # TODO: Replace temporary name
    s3_bucket_output = "criobe-images-reframed"
    s3_model_bucket = "criobe-models-rotate-crop"
    s3_model_name = "detectron2-reframe.pth"

    # Get input image object & bucket from event
    s3_image_input = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8'
    )

    s3_bucket_input = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['bucket']['name'], encoding='utf-8'
    )

    # Download image to container
    with open(image_path, 'wb') as f:
        s3_client.download_fileobj(s3_bucket_input, s3_image_input, f)

    # Download model to container
    with open(m_path, 'wb') as f:
        s3_client.download_fileobj(s3_model_bucket, s3_model_name, f)

    # Reframe
    reframe(m_path, image_path)

    # Save new image to S3
    s3_client.upload_file(output_path, s3_bucket_output, s3_image_output)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application-json"
        },
        "body": {
            "image-bucket": s3_bucket_output,
            "image-object": s3_image_output
        }
    }


def reframe(model_path, file, newSize=400):
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

    name = '/tmp/output.jpg'
    cv2.imwrite(name, warped)
