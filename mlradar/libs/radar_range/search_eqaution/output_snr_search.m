function snr = output_snr_search(power_aperture, system_temperature, noise_factor, losses, target_range, search_volume, scan_time, target_rcs)
%% Calculate the output signal to noise ratio for the search radar range equation.
%     :param power_aperture: The power aperture product (W m^2).
%     :param system_temperature: The system temperature (K).
%     :param noise_factor: The receiver noise factor.
%     :param losses: The system losses.
%     :param target_range: The target distance from the transmitting antenna (m).
%     :param search_volume: The volume to search (steradians).
%     :param scan_time: The time to scan the volume (s).
%     :param target_rcs: The target radar cross section (m^2).
%     :return: The output signal to noise ratio.
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Boltzmann's constant
k = 1.38064852e-23;

% Calculate the output signal to noise ratio
snr = (power_aperture * target_rcs * scan_time) ./ ((4.0 * pi) ^ 3 * k * system_temperature * noise_factor * losses * target_range .^ 4 * search_volume);