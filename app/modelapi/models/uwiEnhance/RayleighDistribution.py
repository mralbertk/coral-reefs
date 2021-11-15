"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

import numpy as np
from models.uwiEnhance.helpers.colorEqualisation import RGB_equalisation
from models.uwiEnhance.helpers.globalStretchingRGB import stretching
from models.uwiEnhance.helpers.hsvStretching_2 import HSVStretching
from models.uwiEnhance.helpers.rayleighDistribution import rayleighStretching
from models.uwiEnhance.helpers.sceneRadianceRGB import sceneRadianceRGB


def rayleigh_distribution(img):
    height = len(img)
    width = len(img[0])

    sceneRadiance = RGB_equalisation(img, height, width)
    sceneRadiance = stretching(sceneRadiance)
    sceneRadiance_Lower, sceneRadiance_Upper = rayleighStretching(sceneRadiance, height, width)
    sceneRadiance = (np.float64(sceneRadiance_Lower) + np.float64(sceneRadiance_Upper)) / 2
    sceneRadiance = HSVStretching(sceneRadiance)
    sceneRadiance = sceneRadianceRGB(sceneRadiance)

    return sceneRadiance