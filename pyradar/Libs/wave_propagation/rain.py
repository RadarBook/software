"""
Project: RadarBook
File: rain.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm
"""
from scipy import log10, exp, array, cos


def attenuation(frequency, rain_rate, elevation_angle, polarization_tilt_angle):
    """
    Calculate the attenuation due to rain.
    :param frequency: The operating frequency (GHz).
    :param rain_rate: The rain rate (mm/hr).
    :param elevation_angle: The elevation angle (radians).
    :param polarization_tilt_angle: The polarization tilt angle (radians).
    :return: The specific attenuation due to rain (dB/km).
    """

    # Table 2.3 Coefficients for calculating k_h
    a_kh = array([-5.33980, -0.35351, -0.23789, -0.94158])
    b_kh = array([-0.1008, 1.26970, 0.86036, 0.64552])
    c_kh = array([1.13098, 0.45400, 0.15354, 0.16817])
    d_kh = -0.18961
    e_kh = 0.71147

    # Table 2.4 Coefficients for calculating k_v
    a_kv = array([-3.80595, -3.44965, -0.39902, 0.50167])
    b_kv = array([0.56934, -0.22911, 0.73042, 1.07319])
    c_kv = array([0.81061, 0.51059, 0.11899, 0.27195])
    d_kv = -0.16398
    e_kv = 0.63297

    # Table 2.5 Coefficients for calculating alpha_h
    a_ah = array([-0.14318, 0.29591, 0.32177, -5.37610, 16.1721])
    b_ah = array([1.82442, 0.77564, 0.63773, -0.96230, -3.29980])
    c_ah = array([-0.55187, 0.19822, 0.13164, 1.47828, 3.43990])
    d_ah = 0.67849
    e_ah = -1.95537

    # Table 2.6 Coefficients for calculating alpha_v
    a_av = array([-0.07771, 0.56727, -0.20238, -48.2991, 48.5833])
    b_av = array([2.33840, 0.95545, 1.14520, 0.791669, 0.791459])
    c_av = array([-0.76284, 0.54039, 0.26809, 0.116226, 0.116479])
    d_av = -0.053739
    e_av = 0.83433

    # Calculate k_h
    k_h = d_kh * log10(frequency) + e_kh
    for a, b, c in zip(a_kh, b_kh, c_kh):
        k_h += a * exp(-((log10(frequency) - b) / c) ** 2)

    k_h = 10**k_h

    # Calculate k_v
    k_v = d_kv * log10(frequency) + e_kv
    for a, b, c in zip(a_kv, b_kv, c_kv):
        k_v += a * exp(-((log10(frequency) - b) / c) ** 2)

    k_v = 10**k_v

    # Calculate alpha_h
    alpha_h = d_ah * log10(frequency) + e_ah
    for a, b, c in zip(a_ah, b_ah, c_ah):
        alpha_h += a * exp(-((log10(frequency) - b) / c) ** 2)

    # Calculate alpha_v
    alpha_v = d_av * log10(frequency) + e_av
    for a, b, c in zip(a_av, b_av, c_av):
        alpha_v += a * exp(-((log10(frequency) - b) / c) ** 2)

    # Calculate k and alpha based on elevation angle and polarization
    k = 0.5 * (k_h + k_v + (k_h - k_v) * cos(elevation_angle)**2 * cos(2. * polarization_tilt_angle))
    alpha = 0.5 * (k_h * alpha_h + k_v * alpha_v + (k_h * alpha_h - k_v * alpha_v) * cos(elevation_angle)**2 *
                   cos(2. * polarization_tilt_angle)) / k

    return k * rain_rate**alpha
