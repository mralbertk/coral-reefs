"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiEnhance.helpers.sceneRadianceHE import RecoverHE


def he(img):
    return RecoverHE(img)