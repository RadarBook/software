"""
Project: RadarBook
File: prn_code.py
Created by: Lee A. Harrison
One: 1/25/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""


def mls(register_length, feedback_taps):
    """
    Generate a maximum length sequence based on the register length and feedback taps.
    :param register_length: The length of the linear feedback shift register.
    :param feedback_taps: The bits to use as feedback.
    :return: The maximum length sequence.
    """
    # Initialize the linear feedback shift register
    register = [i % 2 for i in range(register_length)]

    # For the output sequence
    sequence = []

    # Generate the output PRN based on the register length
    for i in range(2 ** register_length - 1):

        # Calculate the feedback based on the taps and modulo 2 addition
        s = sum([register[i - 1] for i in feedback_taps]) % 2

        # Shift bits to the rights
        for k in reversed(range(len(register[1:]))):
            register[k + 1] = register[k]

        # Stored feedback into bit 0
        register[0] = s

        # Append the output sequence
        sequence.append(register[register_length - 1])

    return [-1 if x == 0 else x for x in sequence]
