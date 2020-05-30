"""
Project: RadarBook
File: rounded_nose_cone.py
Created by: Lee A. Harrison
One: 11/24/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import sin, cos
from scipy.constants import c, pi


def radar_cross_section(frequency, cone_half_angle, nose_radius, incident_angle):
    """
    Calculate the radar cross section of a cone with a rounded nose.
    :param frequency: The frequency of the incident energy (Hz).
    :param cone_half_angle: The half angle of the cone (rad).
    :param nose_radius: The radius of the nose (m).
    :param incident_angle: The incident angle (rad).
    :return: The radar cross section of the rounded nose cone (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    # Wavenumber
    k = 2.0 * pi / wavelength

    # For equations
    sa = 1.0 - sin(cone_half_angle)
    c2 = cos(cone_half_angle) ** 2
    c4 = c2 ** 2
    al = cone_half_angle
    b = nose_radius
    ti = incident_angle
    kb = k * b

    # Calculate the coefficients
    a1 = 2 + 2 * al ** 2 - 2 * ti ** 2 + al ** 4 - al ** 2 * ti ** 2 + 0.5 * ti ** 4 + 2 * al ** 4 * ti ** 2 + \
         4 * kb ** 2 - 2 * kb **2 * ti ** 2 - 8 * kb ** 3 * ti ** 2 + kb ** 2 * ti ** 4 + \
         6 * kb ** 2 * al ** 2 * ti ** 2 + 8 * kb ** 3 * ti ** 4 + 13 * kb ** 4 * ti ** 4

    a2 = -2 - 2 * al ** 2 + 2 * ti ** 2 + al ** 2 * ti ** 2 - 0.5 * ti ** 4 - 6 * kb ** 2 * ti ** 2 + \
         8 * kb ** 4 * ti ** 3 + 3 * kb ** 2 * ti ** 4

    a3 = -4 * (1 + al ** 2 - 0.5 * ti ** 2 + 3 * (kb * ti) ** 2) * (kb * kb * ti ** 2 - (kb * ti) ** 2) - \
         4 * (kb * ti) ** 3

    # Calculate the RCS
    if incident_angle < 1e-12:
        # Axial
        rcs = pi * b ** 2 * (1.0 - sin(2 * k * b * sa) / (k * b * c2) + (1 + c4) / (4 * (k * b) ** 2 * c4)
                             - cos(2 * k * b * sa) / (2 * (k * b) ** 2 * c2))
    else:
        # Non axial
        rcs = pi * (1 + ti ** 2) / (4 * k ** 2) * (a1 + a2 * cos(2 * k * cos(ti) * sa) + a3 * sin(2 * k * cos(ti) * sa))

    return rcs
