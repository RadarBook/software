"""
Project: RadarBook
File: plane_waves.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import pi, mu_0, epsilon_0
from numpy import sqrt, imag, real, sin, cos, arcsin


def parameters(frequency, relative_permittivity, relative_permeability, conductivity):
    """
    Calculate the parameters from Table 2.2.
    :param frequency: The operating frequency (Hz).
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param conductivity: The conductivity (S).
    :return: The parameters listed in Table 2.2.
    """
    # Calculate the angular frequency and material parameters
    omega = 2.0 * pi * frequency
    mu = relative_permeability * mu_0
    epsilon = relative_permittivity * epsilon_0

    # Calculate the propagation constant
    propagation_constant = 1j * omega * sqrt(mu * epsilon) * sqrt(1 - 1j * conductivity / (omega * epsilon))

    # Calculate the phase constant
    phase_constant = imag(propagation_constant)

    # Calculate the attenuation constant
    attenuation_constant = real(propagation_constant)

    # Calculate the wave impedance
    wave_impedance = 1j * omega * mu / propagation_constant

    # Calculate the skin depth
    if attenuation_constant.any() == 0.:
        skin_depth = 0.0
    else:
        skin_depth = 1. / attenuation_constant

    # Calculate the wavelength and phase velocity
    wavelength = 2. * pi / phase_constant
    phase_velocity = omega / phase_constant

    return propagation_constant, phase_constant, attenuation_constant, wave_impedance, skin_depth, \
           wavelength, phase_velocity


def critical_angle(frequency, relative_permittivity, relative_permeability, conductivity):
    """
    Calculate the critical angle for total reflection.
    :param frequency: The operating frequency (Hz).
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param conductivity: The conductivity (S).
    :return: The critical angle (radians).
    """
    # Get the propagation constant for each material
    propagation_constant, _, _, _, _, _, _ = parameters(frequency, relative_permittivity, relative_permeability,
                                                        conductivity)

    return arcsin(propagation_constant[1] / propagation_constant[0]) * 180. / pi


def brewster_angle(frequency, relative_permittivity, relative_permeability, conductivity):
    """
    Calculate the Brewster angle.
    :param frequency: The operating frequency (Hz).
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param conductivity: The conductivity (S).
    :return: The Brewster angle (radians).
    """
    # Get the wave impedance and propagation constant for each material
    propagation_constant, _, _, wave_impedance, _, _, _ = parameters(frequency, relative_permittivity,
                                                                     relative_permeability, conductivity)

    term1 = (wave_impedance[0] / wave_impedance[1])**2

    term2 = (propagation_constant[0] / propagation_constant[1])**2

    return arcsin(sqrt((term1 - 1.) / (term1 - term2))) * 180. / pi


def reflection_transmission(frequency, incident_angle, relative_permittivity, relative_permeability, conductivity):
    """
    Calculate the reflection and transmission coefficients.
    :param frequency:  The operating frequency (Hz).
    :param incident_angle: The incident angle (radians).
    :param relative_permittivity: The relative permittivity.
    :param relative_permeability: The relative permeability.
    :param conductivity: The conductivity (S).
    :return: The reflection and transmission coefficients.
    """
    # Get the wave impedance and propagation constant for each material
    propagation_constant, _, _, wave_impedance, _, _, _ = parameters(frequency, relative_permittivity,
                                                                     relative_permeability, conductivity)

    # Calculate the transmission angle
    transmission_angle = arcsin(propagation_constant[0] / propagation_constant[1] * sin(incident_angle))

    # Calculate the transmission and reflection coefficients for the TE polarization
    reflection_coefficient_te = (wave_impedance[1] * cos(incident_angle) -
                                 wave_impedance[0] * cos(transmission_angle)) / \
                                (wave_impedance[1] * cos(incident_angle) +
                                 wave_impedance[0] * cos(transmission_angle))

    transmission_coefficient_te = (2. * wave_impedance[1] * cos(incident_angle)) / \
                                  (wave_impedance[1] * cos(incident_angle) +
                                   wave_impedance[0] * cos(transmission_angle))

    # Calculate the transmission and reflection coefficients for the TM polarization
    reflection_coefficient_tm = (wave_impedance[1] * cos(transmission_angle) -
                                 wave_impedance[0] * cos(incident_angle)) / \
                                (wave_impedance[1] * cos(transmission_angle) +
                                 wave_impedance[0] * cos(incident_angle))

    transmission_coefficient_tm = (2. * wave_impedance[1] * cos(incident_angle)) / \
                                  (wave_impedance[1] * cos(transmission_angle) +
                                   wave_impedance[0] * cos(incident_angle))

    return reflection_coefficient_te, transmission_coefficient_te, reflection_coefficient_tm, \
           transmission_coefficient_tm
