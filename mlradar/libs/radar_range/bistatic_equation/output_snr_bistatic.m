function snr = output_snr_bistatic(peak_power, transmit_antenna_gain, receive_antenna_gain, transmit_target_range, receive_target_range,...
    frequency, bistatic_target_rcs, system_temperature, bandwidth, noise_factor, transmit_losses, receive_losses)
%% Calculate the bistatic output signal to noise ratio.
%     :param peak_power: The peak transmitted power (W).
%     :param transmit_antenna_gain: The gain of the transmitting antenna.
%     :param receive_antenna_gain: The gain of the receiving antenna.
%     :param transmit_target_range: The range from the transmitting radar to the target (m).
%     :param receive_target_range: The range from the receiving radar to the target (m).
%     :param frequency: The operating frequency (Hz).
%     :param bistatic_target_rcs: The target bistatic radar cross section (m^2).
%     :param system_temperature: The system temperature (K).
%     :param bandwidth: The operating bandwidth (Hz).
%     :param noise_factor: The receiver noise factor.
%     :param transmit_losses: The loss in the transmitter.
%     :param receive_losses: THe loss in the receiver.
%     :return: The output signal to noise ratio for bistatic configurations.
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Speed of light
c = 299792458;

% Boltzmann's constant
k = 1.38064852e-23;

% Calculate the wavelength
wavelength = c / frequency;

% Calculate the output signal to noise ratio
snr = (peak_power * transmit_antenna_gain * receive_antenna_gain * bistatic_target_rcs * wavelength .^ 2) ./ ...
    ((4.0 * pi) ^ 3 * k * system_temperature * bandwidth * noise_factor * transmit_losses * receive_losses *...
    transmit_target_range .^ 2 * receive_target_range .^ 2);