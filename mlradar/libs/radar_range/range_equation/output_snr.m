function snr = output_snr(system_temperature, bandwidth, noise_factor, losses, peak_power, antenna_gain, frequency, target_rcs, target_range)
%% Calculate the signal to noise ratio at the output of the receiver.
%     :param system_temperature: The system temperature (K).
%     :param bandwidth: The operating bandwidth (Hz).
%     :param noise_factor: The receiver noise factor.
%     :param losses: The system losses.
%     :param peak_power: The peak transmitted power (W).
%     :param antenna_gain: The gain of the transmitting antenna.
%     :param frequency: The operating frequency (Hz).
%     :param target_rcs: The target radar cross section (m^2).
%     :param target_range: The target distance from the transmitting antenna (m).
%     :return: The signal to noise ratio at the output of the receiver.
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

% Calculate the output signal to noise ratio
snr = (peak_power * antenna_gain ^ 2 * (c / frequency) ^ 2 * target_rcs) ./ ...
    ((4.0 * pi) ^ 3 * k * system_temperature * bandwidth * noise_factor * losses * target_range .^ 4);