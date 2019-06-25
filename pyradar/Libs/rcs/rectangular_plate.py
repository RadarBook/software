"""
Project: RadarBook
File: rectangular_plate.py
Created by: Lee A. Harrison
On: 10/30/2018
Created with: PyCharm
"""
from scipy import radians, sin, cos, sinc
from scipy.constants import c, pi


def radar_cross_section(frequency, width, length, incident_theta, observation_theta, observation_phi):
    """
    Calculate the bistatic radar cross section for a rectangular plate.
    :param frequency: The frequency of the incident energy (Hz).
    :param width: The width of the plate (m).
    :param length: The length of the plate (m).
    :param incident_theta: The incident angle theta (deg).
    :param observation_theta: The observation angle theta (deg).
    :param observation_phi: The observation angle phi (deg).
    :return: The bistatic radar cross section (m^2).
    """
    # Wavelength
    wavelength = c / frequency

    theta_i = radians(incident_theta)
    theta_o = radians(observation_theta)

    phi_o = radians(observation_phi)

    x = width / wavelength * sin(theta_o) * cos(phi_o)
    y = length / wavelength * (sin(theta_o) * sin(phi_o) - sin(theta_i))

    rcs_tm = 4.0 * pi * (length * width / wavelength) ** 2 * (cos(theta_i) ** 2 * (cos(theta_o) ** 2 * cos(phi_o) ** 2
                                                              + sin(phi_o) ** 2)) * sinc(x) ** 2 * sinc(y) ** 2

    rcs_te = 4.0 * pi * (length * width / wavelength) ** 2 * (cos(theta_o) ** 2 * sin(phi_o) ** 2
                                                              + cos(phi_o) ** 2) * sinc(x) ** 2 * sinc(y) ** 2

    return rcs_tm, rcs_te
