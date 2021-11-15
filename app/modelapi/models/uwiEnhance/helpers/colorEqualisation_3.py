"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

import numpy as np


def cal_equalisation(img, ratio):
    Array = img * ratio
    Array = np.clip(Array, 0, 255)
    return Array


def RGB_equalisation(img):
    img = np.float32(img)
    avg_RGB = []

    for i in range(3):
        avg = np.mean(img[:, :, i])
        avg_RGB.append(avg)

    a_r = avg_RGB[0] / avg_RGB[2]
    a_g = avg_RGB[0] / avg_RGB[1]
    ratio = [0, a_g, a_r]

    for i in range(1, 3):
        img[:, :, i] = cal_equalisation(img[:, :, i], ratio[i])

    return img
