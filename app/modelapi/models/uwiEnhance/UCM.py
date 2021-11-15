"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiEnhance.helpers.colorEqualisation_3 import RGB_equalisation
from models.uwiEnhance.helpers.globalHistogramStretching_2 import stretching
from models.uwiEnhance.helpers.hsvStretching import HSVStretching
from models.uwiEnhance.helpers.sceneRadianceRGB import sceneRadianceRGB


def ucm(img):
    sceneRadiance = RGB_equalisation(img)
    sceneRadiance = stretching(sceneRadiance)
    sceneRadiance = HSVStretching(sceneRadiance)
    sceneRadiance = sceneRadianceRGB(sceneRadiance)

    return sceneRadiance