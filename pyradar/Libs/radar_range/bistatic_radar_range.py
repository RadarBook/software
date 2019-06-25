"""
Project: RadarBook
File: bistatic_radar_range.py
Created by: Lee A. Harrison
On: 6/20/2018
Created with: PyCharm
"""
from scipy.constants import c, pi, Boltzmann as k
from scipy import cos


def power_at_radar(peak_power, transmit_antenna_gain, receive_antenna_gain, transmit_target_range, receive_target_range,
                   frequency, bistatic_target_rcs):
    """
    Calculate the power at the radar for bistatic configurations.
    :param peak_power: The peak transmitted power (W).
    :param transmit_antenna_gain: The gain of the transmitting antenna.
    :param receive_antenna_gain: The gain of the receiving antenna.
    :param transmit_target_range: The range from the transmitting radar to the target (m).
    :param receive_target_range: The range from the receiving radar to the target (m).
    :param frequency: The operating frequency (Hz).
    :param bistatic_target_rcs: The target bistatic radar cross section (m^2).
    :return: The power at the radar for the bistatic case (W).
    """
    # Calculate the wavelength
    wavelength = c / frequency

    return (peak_power * transmit_antenna_gain * receive_antenna_gain * bistatic_target_rcs * wavelength ** 2) / \
           ((4.0 * pi) ** 3 * transmit_target_range ** 2 * receive_target_range ** 2)


def output_snr(peak_power, transmit_antenna_gain, receive_antenna_gain, transmit_target_range, receive_target_range,
               frequency, bistatic_target_rcs, system_temperature, bandwidth, noise_factor, transmit_losses,
               receive_losses):
    """
    Calculate the bistatic output signal to noise ratio.
    :param peak_power: The peak transmitted power (W).
    :param transmit_antenna_gain: The gain of the transmitting antenna.
    :param receive_antenna_gain: The gain of the receiving antenna.
    :param transmit_target_range: The range from the transmitting radar to the target (m).
    :param receive_target_range: The range from the receiving radar to the target (m).
    :param frequency: The operating frequency (Hz).
    :param bistatic_target_rcs: The target bistatic radar cross section (m^2).
    :param system_temperature: The system temperature (K).
    :param bandwidth: The operating bandwidth (Hz).
    :param noise_factor: The receiver noise factor.
    :param transmit_losses: The loss in the transmitter.
    :param receive_losses: THe loss in the receiver.
    :return: The output signal to noise ratio for bistatic configurations.
    """
    # Calculate the wavelength
    wavelength = c / frequency

    return (peak_power * transmit_antenna_gain * receive_antenna_gain * bistatic_target_rcs * wavelength ** 2) / \
           ((4.0 * pi) ** 3 * k * system_temperature * bandwidth * noise_factor * transmit_losses * receive_losses *
            transmit_target_range ** 2 * receive_target_range ** 2)


def output_snr_polar(peak_power, transmit_antenna_gain, receive_antenna_gain, r, theta, separation_distance,
                     frequency, bistatic_target_rcs, system_temperature, bandwidth, noise_factor, transmit_losses,
                     receive_losses):
    """
    Calculate the bistatic output signal to noise ratio.
    :param peak_power: The peak transmitted power (W).
    :param transmit_antenna_gain: The gain of the transmitting antenna.
    :param receive_antenna_gain: The gain of the receiving antenna.
    :param r: The range from the origin to the target (m).
    :param theta: The angle from the "x" axis to the target (rad).
    :param separation_distance: The distance from the transmitter to the receiver (m).
    :param frequency: The operating frequency (Hz).
    :param bistatic_target_rcs: The target bistatic radar cross section (m^2).
    :param system_temperature: The system temperature (K).
    :param bandwidth: The operating bandwidth (Hz).
    :param noise_factor: The receiver noise factor.
    :param transmit_losses: The loss in the transmitter.
    :param receive_losses: THe loss in the receiver.
    :return: The output signal to noise ratio for bistatic configurations.
    """
    # Calculate the wavelength
    wavelength = c / frequency

    # Calculate the range product
    range_product = (r ** 2 + (0.5 * separation_distance) ** 2) ** 2 - (r * separation_distance * cos(theta)) ** 2

    return (peak_power * transmit_antenna_gain * receive_antenna_gain * bistatic_target_rcs * wavelength ** 2) / \
           ((4.0 * pi) ** 3 * k * system_temperature * bandwidth * noise_factor * transmit_losses * receive_losses *
            range_product)
