"""
Project: RadarBook
File: coherent_integration.py
Created by: Lee A. Harrison
One: 10/11/2018
Created with: PyCharm
"""
from scipy import sqrt, log, exp
from Libs.detection.single_pulse import Q


def probability_of_detection(signal_to_noise, number_of_pulses, probability_of_false_alarm, swerling_type):
    """
    Calculate the probability of detection using coherent integration.
    :param signal_to_noise: The signal to noise ratio.
    :param number_of_pulses: The number of pulses to be coherently integrated.
    :param probability_of_false_alarm: The probability of false alarm.
    :param swerling_type: The Swerling target type (0, 1, or 3).
    :return: The probability of detection.
    """
    # Calculate the probability of detection based on the Swerling type
    if swerling_type == 'Swerling 0':
        if isinstance(signal_to_noise, float):
            return Q(sqrt(2.0 * number_of_pulses * signal_to_noise), sqrt(-2.0 * log(probability_of_false_alarm)), 1e-6)
        return [Q(sqrt(2.0 * number_of_pulses * s), sqrt(-2.0 * log(probability_of_false_alarm)), 1e-6) for s in signal_to_noise]
    elif swerling_type == 'Swerling 1':
        if isinstance(signal_to_noise, float):
            return exp(log(probability_of_false_alarm) / (number_of_pulses * signal_to_noise + 1.0))
        return [exp(log(probability_of_false_alarm) / (number_of_pulses * s + 1.0)) for s in signal_to_noise]
    elif swerling_type == 'Swerling 3':
        if isinstance(signal_to_noise, float):
            return (1.0 - (2.0 * number_of_pulses * log(probability_of_false_alarm)) /
                    (2.0 + number_of_pulses * signal_to_noise) ** 2) * exp((2.0 * log(probability_of_false_alarm)) /
                                                                           (2.0 + number_of_pulses * signal_to_noise))
        return [(1.0 - (2.0 * number_of_pulses * log(probability_of_false_alarm)) /
                    (2.0 + number_of_pulses * s) ** 2) *
                exp((2.0 * log(probability_of_false_alarm)) / (2.0 + number_of_pulses * s)) for s in signal_to_noise]
