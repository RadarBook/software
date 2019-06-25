"""
Project: RadarBook
File: finite_length_dipole.py
Created by: Lee A. Harrison
On: 1/22/2018
Created with: PyCharm
"""
from scipy.constants import c, pi, mu_0, epsilon_0
from scipy import euler_gamma, log, sin, cos, exp, sqrt, linspace, finfo
from scipy.special import sici


def directivity(frequency, length, current):
    """
    The directivity of a finite length dipole antenna.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :param current: The peak current on the dipole (A).
    :return: The directivity of a small dipole antenna.
    """
    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Calculate the wave number times the length
    kl = 2.0 * pi * frequency / c * length

    # Calculate the radiation intensity factor
    factor = eta * abs(current) ** 2 / (8.0 * pi ** 2)

    # Calculate the power radiated
    power_radiated = radiated_power(frequency, length, current)

    # Calculate the maximum of the radiation intensity
    theta = linspace(finfo(float).eps, 2.0 * pi, 10000)
    u_max = max(((cos(0.5 * kl * cos(theta)) - cos(0.5 * kl)) / sin(theta)) ** 2)

    return 4.0 * pi * factor * u_max / power_radiated


def beamwidth(frequency, length):
    """
    The half power beamwidth of a finite length dipole antenna.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :return: The half power beamwidth of a small dipole antenna (deg).
    """
    # Calculate the wavenumber times the length
    kl = 2.0 * pi * frequency / c * length

    # Calculate the normalized radiation intensity
    theta = linspace(finfo(float).eps, 2.0 * pi, 10000)
    f = ((cos(0.5 * kl * cos(theta)) - cos(0.5 * kl)) / sin(theta)) ** 2
    g = f / max(f)

    for iT, iU in zip(theta, g):
        if iU >= 0.5:
            theta_half = 0.5 * pi - iT
            break

    return 2.0 * theta_half * 180.0 / pi


def maximum_effective_aperture(frequency, length, current):
    """
    Calculate the maximum effective aperture of a finite length dipole antenna.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :param current: The peak current on the dipole (A).
    :return: The maximum effective aperture (m^2).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    return wavelength ** 2 / (4.0 * pi) * directivity(frequency, length, current)


def radiation_resistance(frequency, length):
    """
    Calculate the radiation resistance for a finite length dipole.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :return: The radiation resistance (Ohms).
    """
    # Calculate the wave number times the length
    kl = 2.0 * pi * frequency / c * length

    # Calculate the sin and cos integrals for this frequency and length
    si, ci = sici(kl)
    si2, ci2 = sici(2.0 * kl)

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Calculate and return the radiation resistance
    return eta / (2.0 * pi) * (euler_gamma + log(kl) - ci + 0.5 * sin(kl) * (si2 - 2.0 * si) + 0.5 * cos(kl) *
                               (euler_gamma + log(0.5 * kl) + ci2 - 2.0 * ci))


def radiated_power(frequency, length, current):
    """
    Calculate the power radiated by a finite length dipole.
    :param frequency: The operating frequency (Hz).
    :param length: The length of the dipole (m).
    :param current: The current on the dipole (A).
    :return: The radiated power (W)
    """
    return 0.5 * radiation_resistance(frequency, length) * abs(current) ** 2


def far_field(frequency, length, current, r, theta):
    """
    Calculate the electric and magnetic far fields for a finite length dipole.
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
    e_theta = 1j * 0.5 * eta * current / (pi * r) * (cos(0.5 * k * length * cos(theta)) - cos(0.5 * k * length)) /\
              sin(theta) * exp(-1j * k * r)

    # Define the phi-component of the electric far field (V/m)
    e_phi = 0.0

    # Define the r-component of the magnetic far field (A/m)
    h_r = 0.0

    # Define the theta-component of the magnetic far field (A/m)
    h_theta = 0.0

    # Define the phi-component of the magnetic far field (A/m)
    h_phi = 1j * 0.5 * current / (pi * r) * (cos(0.5 * k * length * cos(theta)) - cos(0.5 * k * length)) /\
            sin(theta) * exp(-1j * k * r)

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi
