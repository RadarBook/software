"""
Project: RadarBook
File: lla_to_ecef.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import sqrt, sin, cos


def convert(lat, lon, alt):
    """
    Convert coordinates in LLA to ECEF.
    :param lat: The latitude of the point (rad).
    :param lon: The Longitude of the point (rad).
    :param alt: The altitude of the point (m).
    :return: The ECEF coordinates of the point (m).
    """
    # Earth constants
    effective_earth_radius = 6378137
    earth_eccentricity = 8.1819190842622e-2

    # Radius of curvature
    radius = effective_earth_radius / sqrt(1. - earth_eccentricity ** 2 * sin(lat) ** 2)

    # Calculate the coordinates
    ecef_x = (radius + alt) * cos(lat) * cos(lon)
    ecef_y = (radius + alt) * cos(lat) * sin(lon)
    ecef_z = ((1. - earth_eccentricity**2) * radius + alt) * sin(lat)

    return ecef_x, ecef_y, ecef_z
