"""
Project: RadarBook
File: frustum.py
Created by: Lee A. Harrison
One: 11/24/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import sin, cos, arctan, tan
from scipy.constants import c, pi


def radar_cross_section(frequency, nose_radius, base_radius, length, incident_angle):
    """
    Calculate the radar cross section of a frustum.
    :param frequency: The operating frequency (Hz).
    :param nose_radius: The radius of the nose (m).
    :param base_radius: The radius of the base (m).
    :param length: The length (m).
    :param incident_angle: The incident angle (rad).
    :return: The radar cross section of the frustum (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    # Wavenumber
    k = 2.0 * pi / wavelength

    # Calculate the half cone angle
    half_cone_angle = arctan((base_radius - nose_radius) / length)

    # Calculate the heights
    z2 = base_radius * tan(half_cone_angle)
    z1 = nose_radius * tan(half_cone_angle)

    # Calculate the RCS
    if abs(incident_angle - (0.5 * pi + half_cone_angle)) < 1e-12:
        # Specular
        rcs = 8.0 / 9.0 * pi * (z2 ** 1.5 - z1 ** 1.5) ** 2 * sin(half_cone_angle) / \
              (wavelength * cos(half_cone_angle) ** 4)
    elif incident_angle < 1e-3:
        rcs = wavelength ** 2 * (k * base_radius) ** 4 / (4.0 * pi)
    elif pi - incident_angle < 1e-3:
        rcs = wavelength ** 2 * (k * nose_radius) ** 4 / (4.0 * pi)
    else:
        rcs = wavelength * base_radius / (8.0 * pi * sin(incident_angle)) * (tan(incident_angle - half_cone_angle)) ** 2

    return rcs
