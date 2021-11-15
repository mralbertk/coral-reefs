"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiEnhance.helpers.globalHistogramStretching import stretching
from models.uwiEnhance.helpers.sceneRadianceRGB import sceneRadianceRGB
from models.uwiEnhance.helpers.hsvStretching import HSVStretching


def icm(img):
    img = stretching(img)

    sceneRadiance = sceneRadianceRGB(img)
    sceneRadiance = HSVStretching(sceneRadiance)
    sceneRadiance = sceneRadianceRGB(sceneRadiance)

    return sceneRadiance