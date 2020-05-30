"""
Project: RadarBook
File: right_circular_cone.py
Created by: Lee A. Harrison
One: 11/24/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import sin, cos, exp, sqrt
from scipy.constants import c, pi


def radar_cross_section(frequency, cone_half_angle, base_radius, incident_angle):
    """
    Calculate the radar cross section of a right circular cone.
    :param frequency: The operating frequency (Hz).
    :param cone_half_angle: The cone half angle (rad).
    :param base_radius: The base radius (m).
    :param incident_angle: The incident angle (rad).
    :return: The radar cross section of a right circular cone (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    # Wavenumber
    k = 2.0 * pi / wavelength

    # Parameter "n"
    n = 1.5 + cone_half_angle / pi

    # Common factor
    if incident_angle != 0.0:
        value = (wavelength ** 2 * k * base_radius) / (4.0 * pi ** 2) * (sin(pi / n) / n) ** 2 / sin(incident_angle)

    # Special case values
    term1 = 1.0 / (cos(pi / n) - cos(3.0 * pi / n))
    term2 = sin(pi / n) * exp(1j * (2.0 * k * base_radius - pi / 4.0)) / \
            (n * sqrt(pi * k * base_radius) * (cos(pi / n) - cos(3.0 * pi / (2.0 * n))) ** 2)
    nose_max = (wavelength ** 2 / pi) * (k * base_radius * sin(pi / n) / n) ** 2 * abs(term1 + term2) ** 2
    spec_max = wavelength ** 2 * 8.0 * pi / 9.0 * (base_radius / wavelength) ** 3 / \
                 (sin(cone_half_angle) ** 2 * cos(cone_half_angle))
    base_max = wavelength ** 2 * (k * base_radius) ** 4 / (4.0 * pi)

    # Calculate the radar cross section
    if incident_angle < 1e-6:
        # Nose on, double diffraction on base
        term1 = 1.0 / (cos(pi / n) - cos(3.0 * pi / n))
        term2 = sin(pi / n) * exp(1j * (2.0 * k * base_radius - pi / 4.0)) / \
                (n * sqrt(pi * k * base_radius) * (cos(pi/n) - cos(3.0 * pi / (2.0 * n))) ** 2)
        rcs_vv = (wavelength ** 2 / pi) * (k * base_radius * sin(pi / n) / n) ** 2 * abs(term1 + term2) ** 2
        rcs_hh = rcs_vv
    elif abs(incident_angle - pi) < 1e-6:
        # Base specular
        rcs_vv = wavelength ** 2 * (k * base_radius) ** 4 / (4.0 * pi)
        rcs_hh = rcs_vv
    elif abs(incident_angle - (0.5 * pi - cone_half_angle)) < 1e-6:
        # Normal to the generator of the cone
        rcs_vv = wavelength ** 2 * 8.0 * pi / 9.0 * (base_radius / wavelength) ** 3 / \
                 (sin(cone_half_angle) ** 2 * cos(cone_half_angle))
        rcs_hh = rcs_vv

    elif 0.0 < incident_angle < cone_half_angle:
        term1 = exp(1j * (2.0 * k * base_radius * sin(incident_angle) - pi / 4.0))
        term2 = 1.0 / (cos(pi / n) - 1.0) - 1.0 / (cos(pi / n) - cos((3.0 * pi - 2.0 * incident_angle) / n))
        term3 = 1.0 / (cos(pi / n) - 1.0) + 1.0 / (cos(pi / n) - cos((3.0 * pi - 2.0 * incident_angle) / n))

        term4 = exp(-1j*(2.0 * k * base_radius * sin(incident_angle) - pi / 4.0))
        term5 = 1.0 / (cos(pi / n) - 1.0) - 1.0 / (cos(pi / n) - cos((3.0 * pi + 2.0 * incident_angle) / n))
        term6 = 1.0 / (cos(pi / n) - 1.0) + 1.0 / (cos(pi / n) - cos((3.0 * pi + 2.0 * incident_angle) / n))

        rcs_vv = value * abs(term1 * term2 + term4 * term5) ** 2
        rcs_hh = value * abs(term1 * term3 + term4 * term6) ** 2

        if rcs_vv > nose_max:
            rcs_vv = nose_max

        if rcs_hh > nose_max:
            rcs_hh = nose_max

    elif cone_half_angle <= incident_angle < 0.5 * pi:
        term1 = 1.0 / (cos(pi / n) - 1.0) - 1.0 / (cos(pi / n) - cos((3.0 * pi - 2.0 * incident_angle) / n))
        term2 = 1.0 / (cos(pi / n) - 1.0) + 1.0 / (cos(pi / n) - cos((3.0 * pi - 2.0 * incident_angle) / n))

        rcs_vv = value * term1 ** 2
        rcs_hh = value * term2 ** 2

        if rcs_vv > 0.8 * spec_max:
            rcs_vv = spec_max * cos(25 * (incident_angle - (0.5 * pi - cone_half_angle)))

        if rcs_hh > 0.8 * spec_max:
            rcs_hh = spec_max * cos(25 * (incident_angle - (0.5 * pi - cone_half_angle)))

    elif 0.5 * pi <= incident_angle < pi:
        term1 = exp(1j * (2.0 * k * base_radius * sin(incident_angle) - pi / 4.0))
        term2 = 1.0 / (cos(pi / n) - 1.0) - 1.0 / (cos(pi / n) - cos((3.0 * pi - 2.0 * incident_angle) / n))
        term3 = 1.0 / (cos(pi / n) - 1.0) + 1.0 / (cos(pi / n) - cos((3.0 * pi - 2.0 * incident_angle) / n))

        term4 = exp(-1j * (2.0 * k * base_radius * sin(incident_angle) - pi / 4.0))
        term5 = 1.0 / (cos(pi / n) - 1.0) - 1.0 / (cos(pi / n) - cos((2.0 * incident_angle - pi) / n))
        term6 = 1.0 / (cos(pi / n) - 1.0) + 1.0 / (cos(pi / n) - cos((2.0 * incident_angle - pi) / n))

        rcs_vv = value * abs(term1 * term2 + term4 * term5) ** 2
        rcs_hh = value * abs(term1 * term3 + term4 * term6) ** 2

        if rcs_vv > base_max:
            rcs_vv = base_max

        if rcs_hh > base_max:
            rcs_hh = base_max

    return rcs_vv, rcs_hh
