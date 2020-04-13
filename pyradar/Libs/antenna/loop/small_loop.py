"""
Project: RadarBook
File: small_loop.py
Created by: Lee A. Harrison
On: 1/22/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import c, pi, mu_0, epsilon_0
from scipy import sin, cos, exp, sqrt


def directivity():
    """
    The directivity of a small loop antenna.
    :return: The directivity.
    """
    return 1.5


def beamwidth():
    """
    The half power beamwidth of a small loop antenna.
    :return: The beamwidth (deg).
    """
    return 90.0


def maximum_effective_aperture(frequency):
    """
    Calculate the maximum effective aperture of an small loop antenna.
    :param frequency: The operating frequency (Hz).
    :return: The maximum effective aperture (m^2).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    return 3.0 * wavelength ** 2 / (8.0 * pi)


def radiation_resistance(frequency, radius):
    """
    Calculate the radiation resistance for a small circular loop.
    :param frequency: The operating frequency (Hz).
    :param radius: The radius of the small circular loop (m).
    :return: The radiation resistance (Ohms).
    """
    # Calculate and return the radiation resistance
    return 20.0 * pi**2 * (2.0 * pi * radius * frequency / c) ** 4


def radiated_power(frequency, radius, current):
    """
    Calculate the power radiated by a small circular loop.
    :param frequency: The operating frequency (Hz).
    :param radius: The radius of the small circular loop (m).
    :param current: The current on the small circular loop (A).
    :return: The radiated power (W).
    """
    return 0.5 * radiation_resistance(frequency, radius) * abs(current) ** 2


def far_field(frequency, radius, current, r, theta):
    """
    Calculate the electric and magnetic far fields for a small circular loop.
    :param r: The range to the field point (m).
    :param theta: The angle to the field point (rad).
    :param frequency: The operating frequency (Hz).
    :param radius: The radius of the small circular loop (m).
    :param current: The current on the small circular loop (A).
    :return: The electric and magnetic far fields (V/m) & (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Define the radial-component of the electric far field (V/m)
    e_r = 0.0

    # Define the theta-component of the electric far field (V/m)
    e_theta = 0.0

    # Define the phi-component of the electric far field (V/m)
    e_phi = (eta * (k * radius)**2 * current / (4.0 * r) * sin(theta) / (1j * k * r) + 1.0) * exp(-1j * k * r)

    # Define the r-component of the magnetic far field (A/m)
    h_r = (1j * k * radius**2 * current / (2.0 * r**2) * cos(theta)/(1j * k * r) + 1.0) * exp(-1j * k * r)

    # Define the theta-component of the magnetic far field (A/m)
    h_theta = -(k * radius)**2 * current / (4.0 * r) * sin(theta) * (1./(1j * k * r) + (1.0 - 1.0 / (k * r)**2)) \
              * exp(-1j * k * r)

    # Define the phi-component of the magnetic far field (A/m)
    h_phi = 0.0

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi
