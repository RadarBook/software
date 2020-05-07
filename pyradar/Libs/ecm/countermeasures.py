"""
Project: RadarBook
File: countermeasures.py
Created by: Lee A. Harrison
One: 2/26/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import pi
from numpy import sqrt, sin


def jammer_to_signal(peak_power, antenna_gain, target_rcs, jammer_range, jammer_bandwidth, effective_radiated_power,
                     target_range, radar_bandwidth, losses, antenna_gain_jammer_direction):
    """
    Calculate the jammer to signal ratio.
    :param peak_power: The peak transmitted power of the radar (W).
    :param antenna_gain: The gain of the radar antenna.
    :param target_rcs: The target radar cross section (m^2).
    :param jammer_range: The range from the radar to the jammer (m).
    :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param target_range: The range to the target (m).
    :param radar_bandwidth: The radar receiver bandwidth (Hz).
    :param losses: The radar losses.
    :param antenna_gain_jammer_direction: The gain of the radar antenna in the direction of the jammer.
    :return: The signal to jammer ratio.
    """
    # Check the bandwidth
    if jammer_bandwidth > radar_bandwidth:
        jammer_bandwidth = radar_bandwidth

    return (effective_radiated_power * 4.0 * pi * target_range ** 4 * radar_bandwidth * losses *
            antenna_gain_jammer_direction) / (peak_power * antenna_gain ** 2 * target_rcs * jammer_bandwidth *
                                              jammer_range ** 2)


def crossover_range_selfscreen(peak_power, antenna_gain, target_rcs, jammer_bandwidth, effective_radiated_power,
                               radar_bandwidth, losses):
    """
    Calculate the crossover range for a self screening jammer.
    :param peak_power: The peak transmitted power of the radar (W).
    :param antenna_gain: The gain of the radar antenna.
    :param target_rcs: The target radar cross section (m^2).
    :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param radar_bandwidth: The radar receiver bandwidth (Hz).
    :param losses: The radar losses.
    :return: The crossover range (m).
    """
    # Check the bandwidth
    if jammer_bandwidth > radar_bandwidth:
        jammer_bandwidth = radar_bandwidth

    return sqrt((peak_power * antenna_gain * target_rcs * jammer_bandwidth) /
                (effective_radiated_power * 4.0 * pi * radar_bandwidth * losses))


def crossover_range_escort(peak_power, antenna_gain, target_rcs, jammer_range, jammer_bandwidth,
                           effective_radiated_power, radar_bandwidth, losses, antenna_gain_jammer_direction):
    """
    Calculate the crossover range for escort jamming.
    :param peak_power: The peak transmitted power of the radar (W).
    :param antenna_gain: The gain of the radar antenna.
    :param target_rcs: The target radar cross section (m^2).
    :param jammer_range: The range from the radar to the jammer (m).
    :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param radar_bandwidth: The radar receiver bandwidth (Hz).
    :param losses: The radar losses.
    :param antenna_gain_jammer_direction: The gain of the radar antenna in the direction of the jammer.
    :return: The crossover range (m).
    """
    # Check the bandwidth
    if jammer_bandwidth > radar_bandwidth:
        jammer_bandwidth = radar_bandwidth

    return ((peak_power * antenna_gain ** 2 * target_rcs * jammer_bandwidth * jammer_range ** 2) /
            (effective_radiated_power * 4.0 * pi * radar_bandwidth * losses * antenna_gain_jammer_direction)) ** 0.25


def burn_through_range_selfscreen(peak_power, antenna_gain, target_rcs, radar_bandwidth, losses, jammer_to_signal_req,
                                  effective_radiated_power, jammer_bandwidth):
    """
    Calculate the burn through range for a self screening jammer.
    :param peak_power: The peak transmitted power of the radar (W).
    :param antenna_gain: The gain of the radar antenna.
    :param target_rcs: The target radar cross section (m^2).
    :param radar_bandwidth: The radar receiver bandwidth (Hz).
    :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param losses: The radar losses.
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param jammer_to_signal_req: The jammer to signal required to perform a specific radar function.
    :return: The burn through range (m).
    """
    # Check the bandwidth
    if jammer_bandwidth > radar_bandwidth:
        jammer_bandwidth = radar_bandwidth

    return sqrt(jammer_to_signal_req * (peak_power * antenna_gain * target_rcs * jammer_bandwidth) /
                (effective_radiated_power * 4.0 * pi * radar_bandwidth * losses))


def burn_through_range_escort(peak_power, antenna_gain, target_rcs, radar_bandwidth, losses, jammer_range,
                       jammer_to_signal_req, effective_radiated_power, jammer_bandwidth, antenna_gain_jammer_direction):
    """
    Calculate the burn through range for escort jamming.
    :param peak_power: The peak transmitted power of the radar (W).
    :param antenna_gain: The gain of the radar antenna.
    :param target_rcs: The target radar cross section (m^2).
    :param radar_bandwidth: The radar receiver bandwidth (Hz).
    :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param losses: The radar losses.
    :param effective_radiated_power: The jammer's effective radiated power (W).
    :param jammer_to_signal_req: The jammer to signal ratio required to perform a specific radar function.
    :param jammer_range: The range from the radar to the jammer (m).
    :param antenna_gain_jammer_direction: The gain of the radar antenna in the direction of the jammer.
    :return: The burn through range (m).
    """
    # Check the bandwidth
    if jammer_bandwidth > radar_bandwidth:
        jammer_bandwidth = radar_bandwidth

    return (jammer_to_signal_req * (peak_power * antenna_gain ** 2 * target_rcs * jammer_range ** 2 * jammer_bandwidth) /
          (effective_radiated_power * antenna_gain_jammer_direction * 4.0 * pi * radar_bandwidth * losses)) ** 0.25


def delay_line(f):
    """
    Calculate the delay line frequency response.
    :param f: The normalized frequency.
    :return: The delay line frequency response.
    """
    return 4.0 * sin(pi * f) ** 2
