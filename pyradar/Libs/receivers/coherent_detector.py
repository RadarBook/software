"""
Project: RadarBook
File: coherent_detector.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import pi, fftpack, exp
from scipy.signal import butter, freqs


def iq(if_signal, center_frequency, bandwidth, sample_frequency, time):
    """
    Calculate the baseband I and Q signals from the IF signal.
    :param if_signal: The input IF signal to the detector.
    :param center_frequency: The center frequency of the IF signal (Hz).
    :param bandwidth: The bandwidth of the IF signal (Hz).
    :param sample_frequency: The sampling rate (Hz).
    :param time: The time vector for the IF signal (s).
    :return: The baseband I and Q signals.
    """
    # Shift the IF signal to baseband by mixing with the oscillator frequency
    in_phase = if_signal * exp(-1j * 2.0 * pi * center_frequency * time)
    quadrature = if_signal * exp(-1j * (2.0 * pi * center_frequency * time + 0.5 * pi))

    # Calculate the spectra
    frequencies = fftpack.fftfreq(int(sample_frequency), 1.0 / sample_frequency)
    i_freq = fftpack.fft(in_phase)
    q_freq = fftpack.fft(quadrature)

    # Use 6th order Butterworth low pass filter
    b, a = butter(6, 2.0 * pi * (0.1 * bandwidth), 'low', analog=True)
    w, h = freqs(b, a, frequencies)

    i_freq = i_freq * h
    q_freq = q_freq * h

    # Calculate the time domain I/Q of the signal
    in_phase = fftpack.ifft(i_freq)
    quadrature = fftpack.ifft(q_freq)

    return in_phase, quadrature
