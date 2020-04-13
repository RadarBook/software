function p_min = minimum_detectable_signal(system_temperature, bandwidth, noise_factor, losses, signal_to_noise)
%% Calculate the minimum detectable signal based upon the SNR at the output of the receiver.
%     :param system_temperature: The system temperature (K).
%     :param bandwidth: The operating bandwidth (Hz).
%     :param noise_factor: The receiver noise factor.
%     :param losses: The system losses.
%     :param signal_to_noise: The minimum output signal to noise ratio.
%     :return: The minimum detectable signal (W).
%
% Created by: Lee A. Harrison
% On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Boltzmann's constant
k = 1.38064852e-23;

% Calculate the minimum detectable signal
p_min = k * system_temperature * bandwidth * noise_factor * losses * signal_to_noise;