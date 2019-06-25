"""
Project: RadarBook
File: frank_code.py
Created by: Lee A. Harrison
One: 1/26/2019
Created with: PyCharm
"""
from scipy.constants import pi
from scipy import exp


def n_phase_code(n):
    """
    Generate an N-phase Frank code sequence.
    :param n: The sequence groups.
    :return: The Frank code sequence (length N^2).
    """
    phi = [2.0 * pi / float(n) * i * j for i in range(n) for j in range(n)]
    return [exp(1j * p) for p in phi]
