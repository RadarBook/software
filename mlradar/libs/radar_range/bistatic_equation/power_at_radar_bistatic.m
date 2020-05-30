function pr = power_at_radar_bistatic(peak_power, transmit_antenna_gain, receive_antenna_gain, transmit_target_range, receive_target_range, frequency, bistatic_target_rcs)
%% Calculate the power at the radar for bistatic configurations.
%     :param peak_power: The peak transmitted power (W).
%     :param transmit_antenna_gain: The gain of the transmitting antenna.
%     :param receive_antenna_gain: The gain of the receiving antenna.
%     :param transmit_target_range: The range from the transmitting radar to the target (m).
%     :param receive_target_range: The range from the receiving radar to the target (m).
%     :param frequency: The operating frequency (Hz).
%     :param bistatic_target_rcs: The target bistatic radar cross section (m^2).
%     :return: The power at the radar for the bistatic case (W).
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Speed of light
c = 299792458;

% Calculate the wavelength
wavelength = c / frequency;

% Calculate the power at the radar
pr = (peak_power * transmit_antenna_gain * receive_antenna_gain * bistatic_target_rcs * wavelength .^ 2) ./ ...
    ((4.0 * pi) ^ 3 * transmit_target_range .^ 2 * receive_target_range .^ 2);