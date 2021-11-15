"""Source: https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration"""

from scipy import stats


def stretchrange(r_array, height, width):

    length = height * width
    R_rray = r_array.flatten()
    R_rray.sort()

    mode = stats.mode(R_rray).mode[0]
    mode_index_before = list(R_rray).index(mode)

    DR_min = (1-0.655) * mode
    SR_max = R_rray[int(-(length - mode_index_before) * 0.005)]

    return DR_min, SR_max, mode