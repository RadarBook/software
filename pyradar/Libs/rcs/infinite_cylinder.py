"""
Project: RadarBook
File: infinite_cylinder.py
Created by: Lee A. Harrison
One: 10/21/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import radians, cos
from scipy.constants import c, pi
from scipy.special import hankel2, jv


def radar_cross_section_3d(frequency, radius, observation_angle, number_of_modes, length):
    """
    Calculate the bistatic radar cross section for a finite length cylinder.
    :param frequency: The frequency of the incident energy (Hz).
    :param radius: The radius of the cylinder (m).
    :param observation_angle: The observation angle (deg).
    :param number_of_modes: The number of terms to take in the summation.
    :param length: The length of the cylinder (m).
    :return: The bistatic radar cross section for the infinite cylinder (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    rcs_te, rcs_tm = radar_cross_section(frequency, radius, observation_angle, number_of_modes)

    value = 2.0 * length ** 2 / wavelength

    return rcs_te * value, rcs_tm * value


def radar_cross_section(frequency, radius, observation_angle, number_of_modes):
    """
    Calculate the bistatic radar cross section for the infinite cylinder.
    :param frequency: The frequency of the incident energy (Hz).
    :param radius: The radius of the cylinder (m).
    :param observation_angle: The observation angle (deg).
    :param number_of_modes: The number of terms to take in the summation.
    :return: The bistatic radar cross section for the infinite cylinder (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    # Wavenumber
    k = 2.0 * pi / wavelength

    modes = range(number_of_modes + 1)

    # Argument for Bessel and Hankel functions
    z = k * radius

    # Initialize the sum
    s_tm = 0
    s_te = 0

    phi = radians(observation_angle)

    for n in modes:
        en = 2.0
        if n == 0:
            en = 1.0

        an = jv(n, z) / hankel2(n, z)

        jp = n * jv(n, z) / z - jv(n + 1, z)
        hp = n * hankel2(n, z) / z - hankel2(n + 1, z)

        bn = -jp / hp

        s_tm += en * an * cos(n * phi)
        s_te += en * bn * cos(n * phi)

    rcs_tm = 2.0 * wavelength / pi * abs(s_tm) ** 2
    rcs_te = 2.0 * wavelength / pi * abs(s_te) ** 2

    return rcs_te, rcs_tm
