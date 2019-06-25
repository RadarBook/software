"""
Project: RadarBook
File: circular_uniform.py
Created by: Lee A. Harrison
On: 7/6/2018
Created with: PyCharm
"""
from scipy.constants import pi, c
from scipy import sin, cos, amax, arange, exp


def array_factor(number_of_elements, radius, frequency, scan_angle_theta, scan_angle_phi, theta, phi):
    """
    Calculate the array factor for a circular uniform array.
    :param number_of_elements: The number of elements in the array.
    :param radius: The radius of the circular loop (m).
    :param frequency: The operating frequency (Hz).
    :param scan_angle_theta: The theta scan angle of the main beam (rad).
    :param scan_angle_phi: The phi scan angle of the main beam (rad).
    :param theta: The theta pattern angle (rad).
    :param phi: The phi pattern angle (rad).
    :return: The array factor of a circular uniform array.
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the angular position of each element
    phi_n = 2.0 * pi / number_of_elements * arange(number_of_elements)

    # Calculate the phase term
    af = 0.0
    for p in phi_n:
        af += exp(1j * (k * radius) * (sin(theta) * cos(phi - p) - sin(scan_angle_theta) * cos(scan_angle_phi - p)))

    return af / amax(af)
