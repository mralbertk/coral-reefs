"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiEnhance.helpers.labStretching import LABStretching
from models.uwiEnhance.helpers.globalStretchingRGB import stretching


def rghs(img):

    sceneRadiance = stretching(img)
    sceneRadiance = LABStretching(sceneRadiance)

    return sceneRadiance