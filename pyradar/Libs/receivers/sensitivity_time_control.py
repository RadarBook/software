"""
Project: RadarBook
File: sensitivity_time_control.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import c
from numpy import linspace


def attenuation(pulse_repetition_frequency, pulse_width):
    """
    Calculate the STC attenuation.
    :param pulse_repetition_frequency: The PRF (Hz).
    :param pulse_width: The pulse width (s).
    :return: The normalized STC attenuation.
    """
    # Calculate the PRI
    pulse_repetition_interval = 1.0 / pulse_repetition_frequency

    # Find the minimum and maximum ranges
    minimum_range = 0.5 * c * pulse_width
    maximum_range = 0.5 * c * pulse_repetition_interval

    # Set up the range array
    receive_range = linspace(0, maximum_range, 1000)

    # Calculate and return the attenuation
    return receive_range, [1.0 / minimum_range ** 3.5 if r < minimum_range else 1.0 / r ** 3.5 for r in receive_range]
