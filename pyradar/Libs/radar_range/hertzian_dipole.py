"""
Project: RadarBook
File: hertzian_dipole.py
Created by: Lee A. Harrison
On: 6/20/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import pi, mu_0, epsilon_0, c
from numpy import sqrt, sin, exp


def electric_field(relative_permittivity, relative_permeability, frequency, current, length, r, theta):
    """
    Calculate the electric far field for the Hertzian dipole.
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param frequency: The operating frequency (Hz).
    :param current: The current on the dipole (A).
    :param length: The length of the dipole (m).
    :param r: The range to the field point (m).
    :param theta: The angle to the field point (radians).
    :return: The electric far field for the Hertzian dipole (theta-hat) (V/m).
    """
    # Calculate the angular frequency and material parameters
    omega = 2.0 * pi * frequency
    mu = relative_permeability * mu_0
    epsilon = relative_permittivity * epsilon_0

    # Calculate the wavenumber
    k = omega / c

    # Calculate the impedance
    eta = sqrt(mu / epsilon)

    return 1j * eta * k * current * length * exp(-1j * k * r) * sin(theta) / (4.0 * pi * r)


def magnetic_field(frequency, current, length, r, theta):
    """
    Calculate the electric far field for the Hertzian dipole.
    :param frequency: The operating frequency (Hz).
    :param current: The current on the dipole (A).
    :param length: The length of the dipole (m).
    :param r: The range to the field point (m).
    :param theta: The angle to the field point (radians).
    :return: The electric far field for the Hertzian dipole (phi-hat) (V/m).
    """
    # Calculate the angular frequency and material parameters
    omega = 2.0 * pi * frequency

    # Calculate the wavenumber
    k = omega / c

    return 1j * k * current * length * exp(-1j * k * r) * sin(theta) / (4.0 * pi * r)


def power_density(relative_permittivity, relative_permeability, frequency, current, length, r, theta):
    """
    Calculate the power density radiated by the Hertzian dipole.
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param frequency: The operating frequency (Hz).
    :param current: The current on the dipole (A).
    :param length: The length of the dipole (m).
    :param r: The range to the field point (m).
    :param theta: The angle to the field point (radians).
    :return: The power density radiated by the Hertzian dipole (W/m^2).
    """
    # Calculate the angular frequency and material parameters
    omega = 2.0 * pi * frequency
    mu = relative_permeability * mu_0
    epsilon = relative_permittivity * epsilon_0

    # Calculate the wavenumber
    k = omega / c

    # Calculate the impedance
    eta = sqrt(mu / epsilon)

    return 0.5 * eta * (k * current * length * sin(theta) / (4.0 * pi * r)) ** 2


def total_radiated_power(relative_permittivity, relative_permeability, frequency, current, length):
    """
    Calculate the total power radiated by the Hertzian dipole.
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param frequency: The operating frequency (Hz).
    :param current: The current on the dipole (A).
    :param length: The length of the dipole (m).
    :return: The total power radiated byt the Hertzian dipole (W).
    """
    # Calculate the material parameters
    mu = relative_permeability * mu_0
    epsilon = relative_permittivity * epsilon_0

    # Calculate the wavelength
    wavelength = c / frequency

    # Calculate the impedance
    eta = sqrt(mu / epsilon)

    return eta * pi / 3.0 * (current * length / wavelength) ** 2


def radiation_intensity(relative_permittivity, relative_permeability, frequency, current, length, theta):
    """
    Calculate the radiation intensity for the Hertzian dipole.
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param frequency: The operating frequency (Hz).
    :param current: The current on the dipole (A).
    :param length: The length of the dipole (m).
    :param theta: The angle to the field point (radians).
    :return: The radiation intensity for the Hertzian dipole (W/steradian).
    """
    # Calculate the angular frequency and material parameters
    omega = 2.0 * pi * frequency
    mu = relative_permeability * mu_0
    epsilon = relative_permittivity * epsilon_0

    # Calculate the wavenumber
    k = omega / c

    # Calculate the impedance
    eta = sqrt(mu / epsilon)

    return 0.5 * eta * (k * current * length * sin(theta) / (4.0 * pi)) ** 2


def directivity(relative_permittivity, relative_permeability, frequency, current, length, theta):
    """
    Calculate the directivity for the Hertzian dipole.
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param frequency: The operating frequency (Hz).
    :param current: The current on the dipole (A).
    :param length: The length of the dipole (m).
    :param theta: The angle to the field point (radians).
    :return: THe directivity of the Hertzian dipole.
    """
    # Get the total radiated power
    power_radiated = total_radiated_power(relative_permittivity, relative_permeability, frequency, current, length)

    return 4.0 * pi * radiation_intensity(relative_permittivity, relative_permeability,
                                          frequency, current, length, theta) / power_radiated
