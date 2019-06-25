"""
Project: RadarBook
File: single_pulse.py
Created by: Lee A. Harrison
One: 10/10/2018
Created with: PyCharm
"""
from scipy import sqrt, log, exp, log10
from scipy.special import erf, erfinv


def pd_gaussian(signal_to_noise, probability_false_alarm):
    """
    Calculate the probability of detection for a given signal to noise ratio and probability of false alarm.
    when the noise is Gaussian (non-coherent detection).
    :param signal_to_noise: The signal to noise ratio.
    :param probability_false_alarm: The probability of false alarm.
    :return: The probability of detection.
    """
    # Calculate the voltage threshold
    voltage_threshold = erfinv(1.0 - 2.0 * probability_false_alarm) * sqrt(2.0)

    # Calculate the signal amplitude based on signal to noise ratio
    amplitude = sqrt(2.0 * signal_to_noise)

    # Calculate the probability of detection
    return 0.5 * (1.0 - erf((voltage_threshold - amplitude) / sqrt(2.0)))


def pd_rayleigh(signal_to_noise, probability_false_alarm):
    """
    Calculate the probability of detection for a given signal to noise ratio and probability of false alarm.
    when the noise is Rayleigh (coherent detection).
    :param signal_to_noise: The signal to noise ratio.
    :param probability_false_alarm: The probability of false alarm.
    :return: The probability of detection.
    """
    # Calculate the probability of detection
    if isinstance(signal_to_noise, float):
        return Q(sqrt(2.0 * signal_to_noise), sqrt(-2.0 * log(probability_false_alarm)), 1e-6)
    return [Q(sqrt(2.0 * s), sqrt(-2.0 * log(probability_false_alarm)), 1e-6) for s in signal_to_noise]


def Q(x, y, eps):
    """
    Marcum's Q function algorithm by Parl.
    :param x: The first argument of the Q function.
    :param y: The second argument of the Q function.
    :param eps: The convergence criteria.
    :return: The evaluation of the Q function of (x, y, eps).
    """
    n = 1

    alpha_n_1 = 0
    d1 = y / x

    if x < y:
        alpha_n_1 = 1
        d1 = x / y

    alpha_n_2 = 0.0
    beta_n_1 = 0.5
    beta_n_2 = 0.0

    dn = d1

    beta_n = 0.0

    while beta_n < 1.0 / eps:
        alpha_n = dn + 2.0 * n / (x * y) * alpha_n_1 + alpha_n_2
        beta_n = 1.0 + 2.0 * n / (x * y) * beta_n_1 + beta_n_2

        dn *= d1

        alpha_n_2 = alpha_n_1
        alpha_n_1 = alpha_n

        beta_n_2 = beta_n_1
        beta_n_1 = beta_n

        n += 1

    if x < y:
        return alpha_n / (2.0 * beta_n) * exp(-(x - y) ** 2 / 2.0)
    return 1.0 - (alpha_n / (2.0 * beta_n) * exp(-(x - y) ** 2 / 2.0))


def snr_reduction(number_of_pulses, signal_to_noise_nci):
    """
    Calculate the required single pulse signal to noise for non-coherent integration (loss method Curry).
    :param number_of_pulses: The number of pulses to be non-coherently integrated.
    :param signal_to_noise_nci: The signal to noise ratio for non-coherent integration.
    :return: The required single pulse signal to noise ratio.
    """
    return 10.0 * log10(signal_to_noise_nci / (2.0 * number_of_pulses) +
           sqrt(signal_to_noise_nci ** 2 / (4.0 * number_of_pulses ** 2) + signal_to_noise_nci / number_of_pulses))


def snr_gain(probability_of_detection, probability_of_false_alarm, number_of_pulses, signal_to_noise_nci):
    """
    Calculate the required single pulse signal to noise for non-coherent integration (gain method Peebles).
    :param probability_of_detection: The probability of detection.
    :param probability_of_false_alarm: The probability of false alarm.
    :param number_of_pulses: The number of pulses to be non-coherently integrated.
    :param signal_to_noise_nci: The signal to noise ratio for non-coherent integration.
    :return: The requried single pulse signal to noise ratio.
    """
    gain = 6.79 * (1.0 + 0.235 * probability_of_detection) * (1.0 + log10(1.0/probability_of_false_alarm) / 46.6) \
           * log10(number_of_pulses) * (1.0 - 0.14 * log10(number_of_pulses) + 0.01831 * log10(number_of_pulses) ** 2)

    return 10.0 * log10(signal_to_noise_nci) - gain


def single_pulse_snr(probability_of_detection, probability_of_false_alarm):
    """
    Calculate the required signal to noise ratio given a probability of detection and probability of false alarm.
    :param probability_of_detection: The probability of detection.
    :param probability_of_false_alarm: The probability of false alarm.
    :return: The required signal to noise ratio.
    """
    # Starting values
    signal_to_noise = 1.0
    delta = 100.0

    # Loop until required SNR is found
    while True:
        if probability_of_detection > pd_rayleigh(signal_to_noise, probability_of_false_alarm):
            signal_to_noise += delta
        else:
            signal_to_noise -= delta

        delta *= 0.5

        if abs(probability_of_detection - pd_rayleigh(signal_to_noise, probability_of_false_alarm)) < 1e-6:
            break

    return signal_to_noise
