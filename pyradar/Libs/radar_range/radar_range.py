"""
Project: RadarBook
File: radar_range.py
Created by: Lee A. Harrison
On: 1/3/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import c, pi, Boltzmann as k


def power_density(peak_power, antenna_gain, target_range):
    """
    Calculate the power density at a point in space.
    :param peak_power: The peak transmitted power (W).
    :param antenna_gain: The gain of the transmitting antenna.
    :param target_range: The target distance from the transmitting antenna (m).
    :return: The power density at the target (W/m^2).
    """
    return peak_power * antenna_gain / (4.0 * pi * target_range ** 2)


def power_at_radar(peak_power, antenna_gain, target_range, frequency, target_rcs):
    """
    Calculate the power at the radar.
    :param peak_power: The peak transmitted power (W).
    :param antenna_gain: The gain of the transmitting antenna.
    :param target_range: The target distance from the transmitting antenna (m).
    :param frequency: The operating frequency (Hz).
    :param target_rcs: The target radar cross section (m^2).
    :return: The power at the radar (W).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    return (peak_power * antenna_gain ** 2 * wavelength ** 2 * target_rcs) / ((4.0 * pi) ** 3 * target_range ** 4)


def minimum_detectable_signal(system_temperature, bandwidth, noise_factor, losses, signal_to_noise):
    """
    Calculate the minimum detectable signal based upon the SNR at the output of the receiver.
    :param system_temperature: The system temperature (K).
    :param bandwidth: The operating bandwidth (Hz).
    :param noise_factor: The receiver noise factor.
    :param losses: The system losses.
    :param signal_to_noise: The minimum output signal to noise ratio.
    :return: The minimum detectable signal (W).
    """
    return k * system_temperature * bandwidth * noise_factor * losses * signal_to_noise


def maximum_range(system_temperature, bandwidth, noise_factor, losses, signal_to_noise, peak_power, antenna_gain,
                  frequency, target_rcs):
    """
    Calculate the maximum range that the radar can detect the target.
    :param system_temperature: The system temperature (K).
    :param bandwidth: The operating bandwidth (Hz).
    :param noise_factor: The receiver noise factor.
    :param losses: The system losses.
    :param signal_to_noise: The operating signal to noise ratio.
    :param peak_power: The peak transmitted power (W).
    :param antenna_gain: The gain of the transmitting antenna.
    :param frequency: The operating frequency (Hz).
    :param target_rcs: The target radar cross section (m^2).
    :return: The maximum range at which a target can be detected (m).
    """
    # First, calculate the minimum detectable signal
    min_signal = minimum_detectable_signal(system_temperature, bandwidth, noise_factor, losses, signal_to_noise)

    return ((peak_power * antenna_gain ** 2 * (c / frequency) ** 2 * target_rcs) /
            ((4.0 * pi) ** 3 * min_signal)) ** 0.25


def output_snr(system_temperature, bandwidth, noise_factor, losses, peak_power, antenna_gain, frequency, target_rcs,
               target_range):
    """
    Calculate the signal to noise ratio at the output of the receiver.
    :param system_temperature: The system temperature (K).
    :param bandwidth: The operating bandwidth (Hz).
    :param noise_factor: The receiver noise factor.
    :param losses: The system losses.
    :param peak_power: The peak transmitted power (W).
    :param antenna_gain: The gain of the transmitting antenna.
    :param frequency: The operating frequency (Hz).
    :param target_rcs: The target radar cross section (m^2).
    :param target_range: The target distance from the transmitting antenna (m).
    :return: The signal to noise ratio at the output of the receiver.
    """
    return (peak_power * antenna_gain ** 2 * (c / frequency) ** 2 * target_rcs) / \
           ((4.0 * pi) ** 3 * k * system_temperature * bandwidth * noise_factor * losses * target_range ** 4)


def loop_gain(reference_range, reference_rcs, reference_snr):
    """
    Calculate the loop gain given the reference range information.
    :param reference_range: Reference range for the radar (m).
    :param reference_rcs: Reference radar cross section for the radar (m^2).
    :param reference_snr: Reference signal to noise ratio for the radar.
    :return: The loop gain for the radar.
    """
    return reference_range ** 4 * reference_snr / reference_rcs
