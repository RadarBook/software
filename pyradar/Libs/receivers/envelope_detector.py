"""
Project: RadarBook
File: envelope_detector.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.signal import hilbert


def envelope(if_signal):
    """
    Calculate the amplitude envelope of the IF signal.
    :param if_signal: The signal at IF.
    :return: The amplitude envelope.
    """
    return abs(hilbert(if_signal))
