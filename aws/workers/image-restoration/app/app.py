import boto3
import cv2
import numpy as np
import urllib.parse
from PIL import Image


def handler(event, context):
    """
    TODO: Add docstring
    """

    # Internal storage configuration
    image_path = "/tmp/image.jpg"
    output_path = "/tmp/output.jpg"

    # Connect to S3 & configure output
    s3_client = boto3.client("s3")
    # s3_image_output = "my_test.jpg"  # TODO: Replace temporary name
    s3_image_output = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8'
    )
    s3_bucket_output = "criobe-images-treated"

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

    # Perform Histogram Equalization
    image = np.array(Image.open(image_path))
    image = cv2.cvtColor(image, cv2.cv2.COLOR_RGB2BGR)

    for i in range(3):
        image[:, :, i] = cv2.equalizeHist(image[:, :, i])

    cv2.imwrite(output_path, image)

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
