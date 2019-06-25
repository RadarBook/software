"""
Project: RadarBook
File: non_coherent_integration.py
Created by: Lee A. Harrison
One: 10/9/2018
Created with: PyCharm
"""
import sys
from scipy import exp, sqrt, finfo
from scipy.special import gammainc, gammaincinv, iv, binom
from Libs.detection.single_pulse import Q


def single_pulse_snr(pd, pfa, number_of_pulses, swerling_type):
    """
    Compute the required signal to noise ratio given a probability of detection and probability of false alarm.
    :param pd: The probability of detection.
    :param pfa: The probability of false alarm.
    :param number_of_pulses: The number of pulses to be integrated.
    :param swerling_type: The Swerling model type.
    :return: The required signal to noise ratio.
    """
    signal_to_noise = 1.0
    delta = 1000.0

    while True:
        if pd > probability_of_detection(signal_to_noise, pfa, number_of_pulses, swerling_type):
            signal_to_noise += delta
        else:
            signal_to_noise -= delta

        if signal_to_noise < 0.0:
            signal_to_noise = 1e-6

        delta *= 0.5

        if abs(pd - probability_of_detection(signal_to_noise, pfa, number_of_pulses, swerling_type)) < 1e-6:
            break

    return signal_to_noise


def threshold_to_noise_ratio(probability_of_false_alarm, number_of_pulses):
    """
    Calculate the threshold to noise ratio.
    :param probability_of_false_alarm: The probability of false alarm.
    :param number_of_pulses: The number of pulses to be non-coherently integrated.
    :return: The threshold to noise ratio.
    """
    return gammaincinv(number_of_pulses, 1.0 - probability_of_false_alarm)


def probability_of_detection(signal_to_noise, probability_of_false_alarm, number_of_pulses, target_type):
    """
    Calculate the probability of detection for Swerling 0 targets.
    :param signal_to_noise: The signal to noise ratio.
    :param probability_of_false_alarm: The probability of false alarm.
    :param number_of_pulses: The number of pulses to be non-coherently integrated.
    :param target_type: The Swerling target type (0, 1, 2, 3, or 4).
    :return: The probability of detection.
    """
    # Calculate the threshold to noise
    threshold_to_noise = threshold_to_noise_ratio(probability_of_false_alarm, number_of_pulses)

    if target_type == 'Swerling 0':
        s = 0

        for n in range(2, number_of_pulses + 1):
            s += (threshold_to_noise / (number_of_pulses * signal_to_noise)) ** (0.5 * (n - 1.0)) \
                 * iv(n-1, 2.0 * sqrt(number_of_pulses * signal_to_noise * threshold_to_noise))

        if s == float('inf'):
            s = sys.float_info.max
        return Q(sqrt(2.0 * number_of_pulses * signal_to_noise), sqrt(2.0 * threshold_to_noise), 1e-6) \
               + exp(-threshold_to_noise - number_of_pulses * signal_to_noise) * s

    elif target_type == 'Swerling 1':
        return 1.0 - gammainc(number_of_pulses - 1 + finfo(float).eps, threshold_to_noise) \
           + (1.0 + 1.0 / (number_of_pulses * signal_to_noise)) ** (number_of_pulses - 1) \
           * gammainc(number_of_pulses - 1 + finfo(float).eps, threshold_to_noise / (1.0 + 1.0 / (number_of_pulses * signal_to_noise))) \
           * exp(-threshold_to_noise / (1.0 + number_of_pulses * signal_to_noise))

    elif target_type == 'Swerling 2':
        return 1.0 - gammainc(number_of_pulses, threshold_to_noise / (1.0 + signal_to_noise))

    elif target_type == 'Swerling 3':
        return (1.0 + 2.0 / (number_of_pulses * signal_to_noise)) ** (number_of_pulses - 2) * \
           (1.0 + threshold_to_noise / (1.0 + 0.5 * number_of_pulses * signal_to_noise)
            - 2.0 * (number_of_pulses - 2.0) / (number_of_pulses * signal_to_noise)) \
           * exp(-threshold_to_noise / (1.0 + 0.5 * number_of_pulses * signal_to_noise))

    elif target_type == 'Swerling 4':
        s = 0

        for k in range(number_of_pulses + 1):
            s += binom(number_of_pulses, k) * (0.5 * signal_to_noise) ** -k \
                * gammainc(2 * number_of_pulses - k, 2 * threshold_to_noise / (signal_to_noise + 2.0))

        if s == float('inf'):
            s = sys.float_info.max

        return 1.0 - (signal_to_noise / (signal_to_noise + 2.0)) ** number_of_pulses * s
