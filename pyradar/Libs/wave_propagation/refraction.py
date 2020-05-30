"""
Project: RadarBook
File: refraction.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import exp, tan, arccos, cos, radians, degrees, array
from scipy import integrate
from scipy.linalg import norm
from Libs.utils import ecef_to_lla, lla_to_ecef


def apparent_elevation(theta_true, height):
    """
    Calculate the apparent elevation of the target.
    :param theta_true: The true elevation angle (degrees).
    :param height: The height of the radar (km).
    :return: The apparent elevation angle of the target (degrees).
    """

    def integrand(z):
        """
        Determine the integrand for calculating the apparent elevation angle.
        :param z: The altitude (km).
        :return: The integrand.
        """

        # Effective radius of the Earth (km)
        re = 6378.137

        # Standard values
        a = 0.000315
        b = 0.1361

        # Refractive index and derivative as a function of altitude
        n_z = 1. + a * exp(-b * z)
        np_z = -(a * b * exp(-b * z))

        # Refractive index at the given height
        n_h = 1. + a * exp(-b * height)

        tan_phi = tan(arccos(((re + height) * n_h) / ((re + z) * n_z) * cos(radians(theta_true))))

        return np_z / (n_z * tan_phi)

    return theta_true - degrees(integrate.romberg(integrand, height, 1000))


def apparent_elevation_approximate(theta_true, height):
    """
    Calculate the apparent elevation angle with the approximate equation.
    :param theta_true: The true elevation angle (degrees).
    :param height: The height of the radar (km).
    :return: The approximated apparent elevation angle (degrees).
    """
    angle_correction = 1. / (1.728 + 0.5411 * theta_true + 0.03723 * theta_true**2 +
                             height * (0.1815 + 0.06272 * theta_true + 0.01380 * theta_true**2) +
                             height**2 * (0.01727 + 0.008288 * theta_true))

    return theta_true + angle_correction


def apparent_range(radar_lla, target_lla):
    """
    Calculate the apparent range due to refraction.
    :param radar_lla: The radar location in LLA (deg, deg, m).
    :param target_lla: The target location in LLA (deg, deg, m).
    :return: The apparent range from the radar to the target (meters).
    """
    # Convert the radar and target locations
    radar_ecef = array(lla_to_ecef.convert(radians(radar_lla[0]), radians(radar_lla[1]), radar_lla[2]))
    target_ecef = array(lla_to_ecef.convert(radians(target_lla[0]), radians(target_lla[1]), target_lla[2]))

    # Standard values
    a = 0.000315
    b = 0.1361

    # Find the vector from the radar to the target
    line_of_sight = target_ecef - radar_ecef

    # Divide the line of sight into many points for the summation
    number_of_points = 1000

    delta = line_of_sight / (number_of_points - 1)

    # Loop over all the points and perform the summation to find the additional length
    s = 0.
    for i_delta in range(number_of_points):
        # Find the altitude of each point
        l = radar_ecef + delta * i_delta
        _, _, altitude = ecef_to_lla.convert(l[0], l[1], l[2])
        s += ((1. + a * exp(-b * altitude / 1.e3)) - 1.) * norm(delta)

    return norm(line_of_sight), s + norm(line_of_sight)
