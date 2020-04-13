"""
Project: RadarBook
File: rectangular_uniform_free_space.py
Created by: Lee A. Harrison
One: 7/8/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import c, pi, mu_0, epsilon_0
from scipy import sin, cos, sinc, exp, sqrt


def beamwidth(width, height, frequency):
    """
    Calculate the beamwidths for a rectangular aperture in fee space.
    with uniform distribution of fields in the aperture.
    :param width: The aperture width (m).
    :param height: The aperture height (m).
    :param frequency: The operating frequency (Hz).
    :return: The half power and first null beamwidths in the E- and H-plane (deg).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    # Calculate the half power beamwidth in the E-plane
    half_power_eplane = 50.6 * wavelength / height

    # Calculate the half power beamwidth in the H-plane
    half_power_hplane = 50.6 * wavelength / width

    # Calculate the first null beamwidth in the E-plane
    first_null_eplane = 114.6 * wavelength / height

    # Calculate the first null beamwidth in the H-plane
    first_null_hplane = 114.6 * wavelength / width

    return half_power_eplane, half_power_hplane, first_null_eplane, first_null_hplane


def directivity(width, height, frequency):
    """
    Calculate the directivity for a rectangular aperture in fee space.
    with uniform distribution of fields in the aperture.
    :param width: The width of the aperture (m).
    :param height: The height of the aperture (m).
    :param frequency: The operating frequency (Hz).
    :return: The directivity for the rectangular aperture.
    """
    # Calculate the wavelength
    wavelength = c / frequency
    return 4.0 * pi * width * height / wavelength ** 2


def side_lobe_level():
    """
    This is a specific value for a rectangular aperture in fee space.
    with uniform distribution of fields in the aperture.
    :return: The side lobe level for both the E- and H-planes (dB).
    """
    return -13.26


def far_fields(width, height, frequency, r, theta, phi):
    """
    Calculate the far zone electric and magnetic fields for a rectangular aperture in fee space.
    with uniform distribution of fields in the aperture.
    :param r: The range to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param width: The width of the aperture (m).
    :param height: The height of the aperture (m).
    :param frequency: The operating frequency (Hz).
    :return: The far zone electric and magnetic fields (V/m), (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Define the radial-component of the electric far field (V/m)
    e_r = 0.0

    # Define the theta-component of the electric far field (V/m)
    e_theta = 1j * width * height * k / (pi * r) * exp(-1j * k * r) * sin(phi) * (1.0 + cos(theta)) * \
              sinc(k * width * 0.5 * sin(theta) * cos(phi)) * sinc(k * height * 0.5 * sin(theta) * sin(phi))

    # Define the phi-component of the electric far field (V/m)
    e_phi = 1j * width * height * k / (pi * r) * exp(-1j * k * r) * cos(phi) * (1.0 + cos(theta)) * \
            sinc(k * width * 0.5 * sin(theta) * cos(phi)) * sinc(k * height * 0.5 * sin(theta) * sin(phi))

    # Define the r-component of the magnetic far field (A/m)
    h_r = 0.0

    # Define the theta-component of the magnetic far field (A/m)
    h_theta = -1j * width * height * k / (pi * eta * r) * exp(-1j * k * r) * cos(phi) * (1.0 + cos(theta)) * \
              sinc(k * width * 0.5 * sin(theta) * cos(phi)) * sinc(k * height * 0.5 * sin(theta) * sin(phi))

    # Define the phi-component of the magnetic far field (A/m)
    h_phi = 1j * width * height * k / (pi * eta * r) * exp(-1j * k * r) * sin(phi) * (1.0 + cos(theta)) * \
            sinc(k * width * 0.5 * sin(theta) * cos(phi)) * sinc(k * height * 0.5 * sin(theta) * sin(phi))

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi
