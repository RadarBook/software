"""
Project: RadarBook
File: frank_code.py
Created by: Lee A. Harrison
One: 1/26/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import pi
from numpy import exp


def n_phase_code(n):
    """
    Generate an N-phase Frank code sequence.
    :param n: The sequence groups.
    :return: The Frank code sequence (length N^2).
    """
    phi = [2.0 * pi / float(n) * i * j for i in range(n) for j in range(n)]
    return [exp(1j * p) for p in phi]
