"""
Project: RadarBook
File: vegetation.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import exp


def attenuation(distance, specific_attenuation, maximum_attenuation):
    """
    Calculate the attenuation due to vegetation.
    :param distance: The distance into the vegetation (meters).
    :param specific_attenuation: The specific attenuation of the vegetation (dB/km).
    :param maximum_attenuation: The maximum attenuation of the vegetation (dB).
    :return: The attenuation due to the vegetation (dB).
    """
    return maximum_attenuation * (1. - exp(-distance * specific_attenuation / maximum_attenuation))
