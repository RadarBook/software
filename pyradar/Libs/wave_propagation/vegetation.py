"""
Project: RadarBook
File: vegetation.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm
"""
from scipy import exp


def attenuation(distance, specific_attenuation, maximum_attenuation):
    """
    Calculate the attenuation due to vegetation.
    :param distance: The distance into the vegetation (meters).
    :param specific_attenuation: The specific attenuation of the vegetation (dB/km).
    :param maximum_attenuation: The maximum attenuation of the vegetation (dB).
    :return: The attenuation due to the vegetation (dB).
    """
    return maximum_attenuation * (1. - exp(-distance * specific_attenuation / maximum_attenuation))
