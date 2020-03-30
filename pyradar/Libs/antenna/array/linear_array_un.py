"""
Project: RadarBook
File: linear_array.py
Created by: Lee A. Harrison
On: 7/31/2018
Created with: PyCharm
"""
import warnings
from scipy.constants import c, pi
from scipy import cos, floor, roll, amax, ones
from scipy.special import binom
from scipy.signal.windows import chebwin, hanning, hamming, blackmanharris, kaiser


def array_factor(number_of_elements, scan_angle, element_spacing, frequency, theta, window_type, side_lobe_level):
    """
    Calculate the array factor for a linear binomial excited array.
    :param window_type: The string name of the window.
    :param side_lobe_level: The sidelobe level for Tschebyscheff window (dB).
    :param number_of_elements: The number of elements in the array.
    :param scan_angle: The angle to which the main beam is scanned (rad).
    :param element_spacing: The distance between elements.
    :param frequency: The operating frequency (Hz).
    :param theta: The angle at which to evaluate the array factor (rad).
    :return: The array factor as a function of angle.
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the phase
    psi = k * element_spacing * (cos(theta) - cos(scan_angle))

    # Calculate the coefficients
    if window_type == 'Uniform':
        coefficients = ones(number_of_elements)
    elif window_type == 'Binomial':
        coefficients = binom(number_of_elements-1, range(0, number_of_elements))
    elif window_type == 'Tschebyscheff':
        warnings.simplefilter("ignore", UserWarning)
        coefficients = chebwin(number_of_elements, at=side_lobe_level, sym=True)
    elif window_type == 'Kaiser':
        coefficients = kaiser(number_of_elements, 6, True)
    elif window_type == 'Blackman-Harris':
        coefficients = blackmanharris(number_of_elements, True)
    elif window_type == 'Hanning':
        coefficients = hanning(number_of_elements, True)
    elif window_type == 'Hamming':
        coefficients = hamming(number_of_elements, True)

    # Calculate the offset for even/odd
    offset = int(floor(number_of_elements / 2))

    # Odd case
    if number_of_elements & 1:
        coefficients = roll(coefficients, offset + 1)
        coefficients[0] *= 0.5
        return sum(coefficients[i] * cos(i * psi) for i in range(offset + 1))
    # Even case
    else:
        coefficients = roll(coefficients, offset)
        return sum(coefficients[i] * cos((i + 0.5) * psi) for i in range(offset))
