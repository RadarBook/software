"""
Project: RadarBook
File: ducting.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import sqrt


def critical_angle(refractivity_gradient, duct_thickness):
    """
    Calculate the critical angle for ducting.
    :param refractivity_gradient: The refractivity gradient (N/km).
    :param duct_thickness: The duct thickness (meters).
    :return: THe critical angle for ducting to occur (radians).
    """

    return sqrt(2.e-6 * abs(refractivity_gradient) * duct_thickness * 1e-3)
