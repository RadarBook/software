"""
Project: RadarBook
File: small_dipole.py
Created by: Lee A. Harrison
On: 1/22/2018
Created with: PyCharm
"""
from scipy.constants import c, pi, mu_0, epsilon_0
from scipy import sin, exp, sqrt


def directivity():
    """
    The directivity of a small dipole antenna.
    :return: The directivity of a small dipole antenna.
    """
    return 1.5


def beamwidth():
    """
    The half power beamwidth of a small dipole antenna.
    :return: The half power beamwidth of a small dipole antenna (deg).
    """
    return 90.0


def maximum_effective_aperture(frequency):
    """
    Calculate the maximum effective aperture of a small dipole antenna.
    :param frequency: The operating frequency (Hz).
    :return: The maximum effective aperture (m^2).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    return 3.0 * wavelength ** 2 / (8.0 * pi)


def radiation_resistance(frequency, length):
    """
    Calculate the radiation resistance for a small dipole.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :return: The radiation resistance (Ohms).
    """
    # Calculate and return the radiation resistance
    return 20.0 * (pi * length * frequency / c) ** 2


def radiated_power(frequency, length, current):
    """
    Calculate the power radiated by a small dipole.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :param current: The current on the dipole (A).
    :return: The radiated power (W).
    """
    return 0.5 * radiation_resistance(frequency, length) * abs(current) ** 2


def far_field(frequency, length, current, r, theta):
    """
    Calculate the electric and magnetic far fields for a small dipole.
    :param r: The range to the field point (m).
    :param theta: The angle to the field point (rad).
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :param current: The current on the dipole (A).
    :return: The electric and magnetic far fields (V/m) & (A/m).
    """
    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Define the radial-component of the electric far field (V/m)
    e_r = 0.0

    # Define the theta-component of the electric far field (V/m)
    e_theta = 1j * eta * k * current * length / (8.0 * pi * r) * sin(theta) * exp(-1j * k * r)

    # Define the phi-component of the electric far field (V/m)
    e_phi = 0.0

    # Define the r-component of the magnetic far field (A/m)
    h_r = 0.0

    # Define the theta-component of the magnetic far field (A/m)
    h_theta = 0.0

    # Define the phi-component of the magnetic far field (A/m)
    h_phi = 1j * k * current * length / (8.0 * pi * r) * sin(theta) * exp(-1j * k * r)

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi
