import boto3, cv2, os, sys
import numpy as np
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer


def handler(event, context):
    """TODO: Docstring"""

    # Internal storage configuration
    image_path = "/tmp/image.jpg"
    output_path = "/tmp/output.jpg"
    mask_path = "/tmp/output-mask.jpg"
    m_path = "/tmp/model.pth"

    # Connect to S3 & configure
    s3_client = boto3.client("s3")

    # Output image name matches input name
    s3_image_output = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8'
    )

    s3_image_output_split = s3_image_output.split(".")
    s3_mask_output = f"{s3_image_output_split[0]}-mask.{s3_image_output_split[-1]}"

    # TODO: Parameterize output bucket
    s3_bucket_output = "criobe-images-segmented"
    s3_bucket_masks = "criobe-images-masks"

    # TODO: Parameterize model path
    s3_model_bucket = "criobe-models-segmentation"
    s3_model_name = "detectron2-classifier.pth"

    # Get input image object & bucket from event
    s3_image_input = s3_image_output

    s3_bucket_input = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['bucket']['name'], encoding='utf-8'
    )

    # Download image to container
    with open(image_path, 'wb') as f:
        s3_client.download_fileobj(s3_bucket_input, s3_image_input, f)

    # Download model to container
    with open(m_path, 'wb') as f:
        s3_client.download_fileobj(s3_model_bucket, s3_model_name, f)

    # Detect corals
    detector = custom_config(model_path=m_path)
    segmentation(detector, image_path, output_path)

    # Save new image & mask to S3
    s3_client.upload_file(output_path, s3_bucket_output, s3_image_output)
    s3_client.upload_file(mask_path, s3_bucket_masks, s3_mask_output)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application-json"
        },
        "body": {
            "image-bucket": s3_bucket_output,
            "image-object": s3_image_output,
            "mask-bucket": s3_bucket_masks,
            "mask-object": s3_mask_output
        }
    }


#   /------------------------------------------------/
#  /            Custom Configuration                /
# /------------------------------------------------/

def custom_config(model_path=None):
    """Load a Detectron2 model.

    Args:
        model_path: A relative path to model.pth

    Returns:
        predictor: A Detectron2 callable ready for inference
    """

    cfg = get_cfg()
    cfg.MODEL.DEVICE = 'cpu'  # comment this line if you can use a GPU

    # get configuration from model_zoo
    config_file = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    cfg.merge_from_file(model_zoo.get_config_file(config_file))

    # initialize weights
    if not model_path:
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(config_file)
    else:
        assert os.path.isfile(model_path), '.pth file not found'
        cfg.MODEL.WEIGHTS = model_path

    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (is_coral).
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set a custom testing threshold

    predictor = DefaultPredictor(cfg)

    return predictor


def segmentation(classifier, infile, outfile):
    """Performs coral detection on an image file.

    Args:
        classifier: A Detectron2 model trained for coral detection.
        infile: A path to a source image on which to perform segmentation.
        outfile: A destination path to write the segmented image to.

    Returns:
        None
    """
    outfile_split = outfile.split(".")
    mask_outfile = f"{''.join(outfile_split[:-1])}-mask.{outfile_split[-1]}"
    img = cv2.imread(infile)
    output = classifier(img)

    # Build binary mask
    masks = 1 * output["instances"].get("pred_masks").numpy()
    bin_mask = np.zeros(img.shape[:-1])
    for mask in masks:
        mask_bin = np.where(mask == False, 0, 255)
        bin_mask += mask_bin


    # Get Segmented Image
    v = Visualizer(img[:, :, ::-1], scale=1.0)
    out = v.draw_instance_predictions(output["instances"])

    # Write results
    cv2.imwrite(outfile, out.get_image()[:, :, ::-1])
    cv2.imwrite(mask_outfile, bin_mask)

