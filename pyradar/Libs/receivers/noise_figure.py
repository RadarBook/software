"""
Project: RadarBook
File: noise_figure.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm
"""
from scipy import log10, prod


def total_noise_figure(gain, noise_figure):
    """
    Calculate the total noise figure for a cascaded network.
    :param gain: The gain of each component (dB).
    :param noise_figure: The noise figure of each component (dB).
    :return: The total noise figure (dB).
    """

    # Convert noise figure and gain to linear units
    noise_factor = [10.0 ** (nf / 10.0) for nf in noise_figure]
    gain_linear = [10.0 ** (g / 10.0) for g in gain]

    # Start with the first component
    total = noise_factor[0]

    # Loop over the remaining components
    i = 1
    for nf in noise_factor[1:]:
        total += (nf - 1.0) / prod(gain_linear[:i])
        i += 1

    # Return the total noise figure
    return 10.0 * log10(total)
