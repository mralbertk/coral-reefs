from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

import os


def custom_config(model_path=None):
    cfg = get_cfg()
    cfg.MODEL.DEVICE = 'cpu'  # comment this line if you can use a GPU

    # get configuration from model_zoo
    config_file = "COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml"
    cfg.merge_from_file(model_zoo.get_config_file(config_file))

    # initialize weights
    if not model_path:
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(config_file)
    else:
        assert os.path.isfile(model_path), '.pth file not found'
        cfg.MODEL.WEIGHTS = model_path

    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (quadrat).
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set a custom testing threshold

    predictor = DefaultPredictor(cfg)

    return predictor