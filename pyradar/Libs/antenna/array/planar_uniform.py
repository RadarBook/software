"""
Project: RadarBook
File: planar_uniform.py
Created by: Lee A. Harrison
On: 1/22/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import pi, sin, cos, divide, ones_like
from scipy.constants import c


def array_factor(number_of_elements_x, number_of_elements_y, element_spacing_x, element_spacing_y, frequency,
                 scan_angle_theta, scan_angle_phi, theta, phi):
    """
    Calculate the array factor for a planar uniform array.
    :param number_of_elements_x: The number of elements in the x-direction.
    :param number_of_elements_y: The number of elements in the y-direction.
    :param element_spacing_x: The spacing of the elements in the x-direction (m).
    :param element_spacing_y: The spacing of the elements in the y-direction (m).
    :param frequency: The operating frequency (Hz).
    :param scan_angle_theta: The scan angle in the theta-direction (rad).
    :param scan_angle_phi: The scan angle in the phi-direction (rad).
    :param theta: The pattern angle in theta (rad).
    :param phi: The pattern angle in phi (rad).
    :return: The array factor for a planar uniform array.
    """
    # Calculate the wave number
    k = 2.0 * pi * frequency / c

    # Calculate the phase
    psi_x = k * element_spacing_x * (sin(theta) * cos(phi) - sin(scan_angle_theta) * cos(scan_angle_phi))
    psi_y = k * element_spacing_y * (sin(theta) * sin(phi) - sin(scan_angle_theta) * sin(scan_angle_phi))

    # Break into numerator and denominator
    numerator = sin(0.5 * number_of_elements_x * psi_x) * sin(0.5 * number_of_elements_y * psi_y)
    denominator = number_of_elements_x * number_of_elements_y * sin(0.5 * psi_x) * sin(0.5 * psi_y)

    return divide(numerator, denominator, ones_like(psi_x), where=(denominator != 0.0)), psi_x, psi_y
