"""
Project: RadarBook
File: binary_integration.py
Created by: Lee A. Harrison
One: 10/11/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.special import binom


def probability_of_detection(m, n, pd):
    """
    Calculate the probability of detection for M of N integration.
    :param m: The number of required detections.
    :param n: The total number of measurements.
    :param pd: The probability of detection for a single measurement.
    :return: The probability of M on N detections.
    """
    return sum([binom(n, k) * pd ** k * (1.0 - pd) ** (n - k) for k in range(m, n + 1)])


def probability_of_false_alarm(m, n, pfa):
    """
    Calcualte the probability of false alarm for M of N integration.
    :param m: The number of required detections.
    :param n: The total number of measurements.
    :param pfa: The probability of false alarm for a single measurement.
    :return: The probability false alarm for M on N detections.
    """
    return sum([binom(n, k) * pfa ** k * (1.0 - pfa) ** (n - k) for k in range(m, n + 1)])
