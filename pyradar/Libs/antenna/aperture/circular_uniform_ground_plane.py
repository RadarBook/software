"""
Project: RadarBook
File: circular_uniform_ground_plane.py
Created by: Lee A. Harrison
One: 7/8/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import c, pi, mu_0, epsilon_0
from scipy import sin, cos, exp, sqrt, divide
from scipy.special import jv


def beamwidth(radius, frequency):
    """
    Calculate the beamwidths for a circular aperture in a ground plane with a uniform distribution of the fields.
    :param radius: The radius of the aperture (m).
    :param frequency: The operating frequency (Hz).
    :return: The half power and first null beamwidths in the E- and H-plane (deg).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    # Calculate the half power beamwidth in the E-plane
    half_power_eplane = 29.2 * wavelength / radius

    # Calculate the half power beamwidth in the H-plane
    half_power_hplane = 29.2 * wavelength / radius

    # Calculate the first null beamwidth in the E-plane
    first_null_eplane = 69.9 * wavelength / radius

    # Calculate the first null beamwidth in the H-plane
    first_null_hplane = 69.9 * wavelength / radius

    return half_power_eplane, half_power_hplane, first_null_eplane, first_null_hplane


def directivity(radius, frequency):
    """
    Calculate the directivity for a circular aperture in a ground plane with a uniform distribution of the fields.
    :param radius: The radius of the aperture (m).
    :param frequency: The operating frequency (Hz).
    :return: The directivity for the circular aperture.
    """
    # Calculate the wavelength
    wavelength = c / frequency
    return (2.0 * pi * radius / wavelength) ** 2


def side_lobe_level():
    """
    This is a specific value for a circular aperture in a ground plane with a uniform distribution of the fields.
    :return: The side lobe level for both the E- and H-planes (dB).
    """
    return -17.6


def far_fields(radius, frequency, r, theta, phi):
    """
    Calculate the electric and magnetic fields in the far field of the aperture.
    :param r: The range to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param radius: The radius of the aperture (m).
    :param frequency: The operating frequency (Hz).
    :return: The electric and magnetic fields radiated by the aperture (V/m), (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Calculate the argument for the Bessel function
    z = k * radius * sin(theta)

    # Calculate the Bessel function
    bessel_term = divide(jv(1, z), z, where=z != 0.0)

    # Define the radial-component of the electric far field (V/m)
    e_r = 0.0

    # Define the theta-component of the electric far field (V/m)
    e_theta = 1j * k * radius ** 2 * exp(-1j * k * r) / r * sin(phi) * bessel_term

    # Define the phi-component of the electric far field (V/m)
    e_phi = 1j * k * radius ** 2 * exp(-1j * k * r) / r * cos(phi) * bessel_term

    # Define the radial-component of the magnetic far field (A/m)
    h_r = 0.0

    # Define the theta-component of the magnetic far field (A/m)
    h_theta = 1j * k * radius ** 2 * exp(-1j * k * r) / r * -cos(theta) * cos(phi) / eta * bessel_term

    # Define the phi-component of the magnetic far field (A/m)
    h_phi = 1j * k * radius ** 2 * exp(-1j * k * r) / r * sin(phi) / eta * bessel_term

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi
