"""
Project: RadarBook
File: infinite_cylinder_oblique.py
Created by: Lee A. Harrison
One: 11/21/2018
Created with: PyCharm
"""
from scipy import radians, cos, sin, sinc
from scipy.constants import c, pi
from scipy.special import hankel2, jv


def radar_cross_section_3d(frequency, radius, incident_angle, observation_angle, number_of_modes, length):
    """
    Calculate the bistatic radar cross section for a finite length cylinder with oblique incidence.
    :param frequency: The frequency of the incident energy (Hz).
    :param radius: The radius of the cylinder (m).
    :param incident_angle: The angle of incidence from z-axis (deg).
    :param observation_angle: The observation angle (deg).
    :param number_of_modes: The number of terms to take in the summation.
    :param length: The length of the cylinder (m).
    :return: The bistatic radar cross section for the infinite cylinder (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    theta_i = radians(incident_angle)
    theta_o = theta_i

    # Calculate the 2D RCS
    rcs_te, rcs_tm = radar_cross_section(frequency, radius, incident_angle, observation_angle, number_of_modes)

    value = 2.0 * length ** 2 / wavelength * sin(theta_o) ** 2 * \
            sinc(length / wavelength * (cos(theta_i) + cos(theta_o))) ** 2

    return rcs_te * value, rcs_tm * value


def radar_cross_section(frequency, radius, incident_angle, observation_angle, number_of_modes):
    """
    Calculate the bistatic radar cross section for the infinite cylinder with oblique incidence.
    :param frequency: The frequency of the incident energy (Hz).
    :param radius: The radius of the cylinder (m).
    :param incident_angle: The angle of incidence from z-axis (deg).
    :param observation_angle: The observation angle (deg).
    :param number_of_modes: The number of terms to take in the summation.
    :return: The bistatic radar cross section for the infinite cylinder (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    # Wavenumber
    k = 2.0 * pi / wavelength

    modes = range(number_of_modes + 1)

    # Initialize the sum
    s_tm = 0
    s_te = 0

    phi = radians(observation_angle)
    theta_i = radians(incident_angle)

    # Argument for Bessel and Hankel functions
    z = k * radius * sin(theta_i)

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

    rcs_tm = 2.0 * wavelength / (pi * sin(theta_i)) * abs(s_tm) ** 2
    rcs_te = 2.0 * wavelength / (pi * sin(theta_i)) * abs(s_te) ** 2

    return rcs_te, rcs_tm
