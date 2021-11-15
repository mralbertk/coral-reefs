"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiColorRestore.helpers.getAtmosphericLight_2 import getAtomsphericLight
from models.uwiColorRestore.helpers.getColorContrastEnhancement import ColorContrastEnhancement
from models.uwiColorRestore.helpers.getRGBDarkChannel import getDarkChannel
from models.uwiColorRestore.helpers.sceneRadiance_2 import SceneRadiance
from models.uwiColorRestore.helpers.getTransmissionMap import getTransmissionMap


def low_complexity_dcp(img, blockSize = 9):

    imgGray = getDarkChannel(img, blockSize)
    AtomsphericLight = getAtomsphericLight(imgGray, img, meanMode=True, percent=0.001)
    transmission = getTransmissionMap(img, AtomsphericLight, blockSize)

    sceneRadiance = SceneRadiance(img, AtomsphericLight, transmission)
    sceneRadiance = ColorContrastEnhancement(sceneRadiance)

    return sceneRadiance
