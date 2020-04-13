"""
Project: RadarBook
File: ambiguity_function.py
Created by: Lee A. Harrison
One: 1/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import sinc, linspace, sqrt, sin, zeros, exp, conj, amax
from scipy.fftpack import fft, ifft, fftshift, next_fast_len
from scipy.constants import pi


def single_pulse(time_delay, doppler_frequency, pulse_width):
    """
    Calculate the ambiguity function for a continuous wave single pulse.
    :param time_delay: The time delay for the ambiguity function (seconds).
    :param doppler_frequency: The Doppler frequency for the ambiguity function (Hz).
    :param pulse_width: The pulse width (seconds).
    :return: The ambiguity function for a CW pulse.
    """
    ambiguity = abs((1.0 - abs(time_delay / pulse_width)) *
                    sinc(doppler_frequency * (pulse_width - abs(time_delay))))**2

    ambiguity[abs(time_delay) > pulse_width] = 0

    return ambiguity


def pulse_train(time_delay, doppler_frequency, pulse_width, pulse_repetition_interval, number_of_pulses):
    """
    Calculate the ambiguity function for a coherent pulse train.
    :param time_delay: The time delay for the ambiguity function (seconds).
    :param doppler_frequency: The Doppler frequency for the ambiguity function (Hz).
    :param pulse_width: The pulse width (seconds).
    :param pulse_repetition_interval: The time between successive pulses (seconds).
    :param number_of_pulses: The total number of pulses.
    :return: The ambiguity function for a coherent pulse train.
    """
    ambiguity = 0

    for q in range(-(number_of_pulses-1), number_of_pulses):

        a1 = sqrt(single_pulse(time_delay - q * pulse_repetition_interval, doppler_frequency, pulse_width))

        ambiguity += a1 * abs(sin(pi * doppler_frequency * (number_of_pulses - abs(q)) * pulse_repetition_interval) /
                              sin(pi * doppler_frequency * pulse_repetition_interval))

    return abs(ambiguity/number_of_pulses)**2


def lfm_pulse(time_delay, doppler_frequency, pulse_width, bandwidth):
    """
    Calculate the ambiguity function for a linear frequency modulated single pulse.
    :param time_delay: The time delay for the ambiguity function (seconds).
    :param doppler_frequency: The Doppler frequency for the ambiguity function (Hz).
    :param pulse_width: The waveform pulse width (seconds).
    :param bandwidth: The waveform band width (Hz).
    :return: The ambiguity function for an LFM pulse.
    """
    ambiguity = abs((1.0 - abs(time_delay) / pulse_width) *
                    sinc(pi * pulse_width * (bandwidth / pulse_width * time_delay + doppler_frequency) *
                    (1.0 - abs(time_delay) / pulse_width)))**2

    ambiguity[abs(time_delay) > pulse_width] = 0

    return ambiguity


def lfm_train(time_delay, doppler_frequency, pulse_width, bandwidth, pulse_repetition_interval, number_of_pulses):
    """
    Calculate the ambiguity function for an LFM pulse train.
    :param time_delay: The time delay for the ambiguity function (seconds).
    :param doppler_frequency: The Doppler frequency for the ambiguity function (Hz).
    :param pulse_width: The waveform pulse width (seconds).
    :param bandwidth: The waveform band width (Hz).
    :param pulse_repetition_interval: The time between successive pulses (seconds).
    :param number_of_pulses: The total number of pulses.
    :return: The ambiguity function for an LFM pulse train.
    """
    ambiguity = 0

    for q in range(-(number_of_pulses - 1), number_of_pulses):
        a1 = sqrt(lfm_pulse(time_delay - q * pulse_repetition_interval, doppler_frequency, pulse_width, bandwidth))

        ambiguity += a1 * abs(sin(pi * doppler_frequency * (number_of_pulses - abs(q)) * pulse_repetition_interval) /
                              sin(pi * doppler_frequency * pulse_repetition_interval))

    return abs(ambiguity / number_of_pulses) ** 2


def phase_coded_wf(code, chip_width):
    """
    Calculate the ambiguity function for phase coded waveforms.
    :param code: The value of each chip (1, -1).
    :param chip_width: The pulsewidth of each chip (s).
    :return: The ambiguity function for a phase coded waveform.
    """
    # Upsample factor
    n_upsample = 100

    # Number of Doppler bins
    n_frequency = 512

    # Code length
    n_code = len(code)

    # Upsample the code
    n_samples = n_upsample * n_code

    # A fast length for the FFT
    n_fft_samples = next_fast_len(4 * n_samples)

    # Initialize the upsampled code
    code_up = zeros([n_fft_samples], dtype=complex)

    for i in range(n_code):
        for j in range(n_upsample):
            code_up[n_upsample * i + j] = code[i]

    # Create the FFT of the extended sequence
    v = conj(fft(code_up))

    # The time delay
    s = 0.5 * (n_fft_samples / n_samples)
    time_delay = linspace(-n_code * chip_width * s, n_code * chip_width * s, n_fft_samples)

    # The Doppler mismatch frequency
    doppler_frequency = linspace(-1 / chip_width, 1 / chip_width, n_frequency)

    # Initialize the ambiguity function
    ambiguity = zeros([n_frequency, n_fft_samples])

    # Create the array of FFTs of the shifted sequence
    for i in range(n_frequency):
        phi = 2.0 * pi * doppler_frequency[i] * time_delay
        u = fft(code_up * exp(1j * phi)) * v
        ambiguity[i, :] = fftshift(abs(ifft(u, n_fft_samples)))

    # Normalize the ambiguity function
    ambiguity /= amax(ambiguity)

    return ambiguity ** 2, time_delay, doppler_frequency
