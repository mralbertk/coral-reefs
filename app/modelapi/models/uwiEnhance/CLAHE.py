"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiEnhance.helpers.sceneRadianceCLAHE import RecoverCLAHE


def clahe(img):
    return RecoverCLAHE(img)