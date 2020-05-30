"""
Project: RadarBook
File: cloud_fog.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""


def attenuation(frequency, liquid_water_temperature, liquid_water_density):
    """
    Calculate the specific attenuation due to cloud or fog.
    :param frequency: The operating frequency (GHz).
    :param liquid_water_temperature: The liquid water temperature (K).
    :param liquid_water_density: The liquid water density (g/m^3)
    :return: The specific attenuation (dB/km)
    """

    # Calculate the relative water temperature
    theta = 300 / liquid_water_temperature

    # Calculate the principal and secondary relaxation frequencies
    fp = 20.20 - 146. * (theta - 1.) + 316. * (theta - 1.)**2
    fs = 39.8 * fp

    # Preliminary calculations for the permittivity
    eps_0 = 77.66 + 103.3 * (theta - 1.)
    eps_1 = 0.0671 * eps_0
    eps_2 = 3.52

    # Calculate the complex permittivity
    eps_p = (eps_0 - eps_1) / (1. + (frequency/fp)**2) + (eps_1 - eps_2) / (1. + (frequency/fs)**2)

    eps_pp = frequency * (eps_0 - eps_1) / (fp * (1. + (frequency/fp)**2)) + \
             frequency * (eps_1 - eps_2) / (fs * (1. + (frequency/fs)**2))

    # Calculate the impedance
    eta = (2. + eps_p) / eps_pp

    # Calculate the specific impedance
    k_l = 0.819 * frequency / (eps_pp * (1 + eta**2))

    return k_l * liquid_water_density
