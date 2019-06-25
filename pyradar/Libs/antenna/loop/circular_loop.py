"""
Project: RadarBook
File: circular_loop.py
Created by: Lee A. Harrison
On: 1/22/2018
Created with: PyCharm
"""
from scipy.constants import c, pi, mu_0, epsilon_0
from scipy import sin, cos, exp, sqrt, linspace, finfo
from scipy.special import j1


def directivity(frequency, radius):
    """
    The directivity of a circular loop antenna.
    :param frequency: The operating frequency (Hz).
    :param radius: The radius of the loop antenna (m).
    :return: The directivity.
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    return 2.0 * k * radius * 0.58 ** 2


def beamwidth(frequency, radius):
    """
    The half power beamwidth of a circular loop antenna.
    :param frequency: The operating frequency (Hz).
    :param radius: The radius of the circular loop (m).
    :return: The beamwidth (deg).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the normalized radiation intensity
    theta = linspace(finfo(float).eps, 2.0 * pi, 10000)
    f = (j1(k * radius * sin(theta))) ** 2
    g = f / max(f)

    for iT, iU in zip(theta, g):
        if iU >= 0.5:
            theta_half = 0.5 * pi - iT
            break

    return 2.0 * theta_half * 180.0 / pi


def maximum_effective_aperture(frequency, radius):
    """
    Calculate the maximum effective aperture of an circular loop antenna.
    :param radius: The radius of the loop antenna (m).
    :param frequency: The operating frequency (Hz).
    :return: The maximum effective aperture (m^2).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    # Calculate the wavenumber
    k = 2.0 * pi / wavelength

    return k * radius * wavelength ** 2 / (4.0 * pi) * 0.58 ** 2


def radiation_resistance(frequency, radius):
    """
    Calculate the radiation resistance for a small circular loop.
    :param frequency: The operating frequency (Hz).
    :param radius: The radius of the small circular loop (m).
    :return: The radiation resistance (Ohms).
    """
    # Calculate and return the radiation resistance
    return 60.0 * pi ** 2 * 2.0 * pi * frequency / c * radius


def radiated_power(frequency, radius, current):
    """
    Calculate the power radiated by a small circular loop.
    :param frequency: The operating frequency (Hz)
    :param radius: The radius of the small circular loop (m).
    :param current: The current on the small circular loop (A)
    :return: The radiated power (W)
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
    e_phi = exp(-1j * k * r) * (eta * k * radius * current) / (2.0 * r) * j1(k * radius * sin(theta))

    # Define the r-component of the magnetic far field (A/m)
    h_r = (1j * k * radius**2 * current / (2.0 * r**2) * cos(theta)/(1j * k * r) + 1.0) * exp(-1j * k * r)

    # Define the theta-component of the magnetic far field (A/m)
    h_theta = -exp(-1j * k * r) * current * k * radius / (2.0 * r) * j1(k * radius * sin(theta))

    # Define the phi-component of the magnetic far field (A/m)
    h_phi = 0.0

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi
