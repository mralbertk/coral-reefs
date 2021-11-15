"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

import numpy as np

from models.uwiColorRestore.helpers.adaptiveExposureMap import AdaptiveExposureMap
from models.uwiColorRestore.helpers.adaptiveSceneRadiance import AdaptiveSceneRadiance
from models.uwiColorRestore.helpers.getAtmosphericLight import getAtomsphericLight
from models.uwiColorRestore.helpers.determineDepth import determineDepth
from models.uwiColorRestore.helpers.refinedTransmission import refinedtransmission
from models.uwiColorRestore.helpers.getTransmission import getTransmission
from models.uwiColorRestore.helpers.sceneRadianceGB import sceneRadianceGB
from models.uwiColorRestore.helpers.sceneRadiance import sceneradiance


# Adaptive Exposure
np.seterr(over='ignore')
np.seterr(invalid ='ignore')
np.seterr(all ='ignore')


def gbdehazingrcoorection(img):

    img = (img - img.min()) / (img.max() - img.min()) * 255

    blockSize = 9

    largestDiff = determineDepth(img, blockSize)

    AtomsphericLight, AtomsphericLightGB, AtomsphericLightRGB = getAtomsphericLight(largestDiff, img)

    transmission = getTransmission(img, AtomsphericLightRGB, blockSize)
    transmission = refinedtransmission(transmission, img)

    sceneRadiance_GB = sceneRadianceGB(img, transmission, AtomsphericLightRGB)
    sceneRadiance = sceneradiance(img, sceneRadiance_GB)

    # TODO: Lambda and blockSize are not used by AdaptiveExposureMap
    S_x = AdaptiveExposureMap(img, sceneRadiance, Lambda=0.3, blockSize=blockSize)
    sceneRadiance = AdaptiveSceneRadiance(sceneRadiance, S_x)

    return sceneRadiance