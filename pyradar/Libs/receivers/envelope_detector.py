"""
Project: RadarBook
File: envelope_detector.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm
"""
from scipy.signal import hilbert


def envelope(if_signal):
    """
    Calculate the amplitude envelope of the IF signal.
    :param if_signal: The signal at IF.
    :return: The amplitude envelope.
    """
    return abs(hilbert(if_signal))
