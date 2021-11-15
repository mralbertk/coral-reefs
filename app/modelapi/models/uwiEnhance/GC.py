"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from models.uwiEnhance.helpers.sceneRadianceGC import RecoverGC


def gc(img):
    return RecoverGC(img)