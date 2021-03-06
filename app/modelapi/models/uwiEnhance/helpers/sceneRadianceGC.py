"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

import numpy as np


def RecoverGC(sceneRadiance):
    sceneRadiance = sceneRadiance/255.0

    for i in range(3):
        sceneRadiance[:, :, i] =  np.power(sceneRadiance[:, :, i] / float(np.max(sceneRadiance[:, :, i])), 0.7)

    sceneRadiance = np.clip(sceneRadiance*255, 0, 255)
    sceneRadiance = np.uint8(sceneRadiance)

    return sceneRadiance