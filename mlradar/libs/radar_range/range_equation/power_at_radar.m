function pr = power_at_radar(peak_power, antenna_gain, target_range, frequency, target_rcs)
%% Calculate the power at the radar.
% :param peak_power: The peak transmitted power (W).
% :param antenna_gain: The gain of the transmitting antenna.
% :param target_range: The target distance from the transmitting antenna (m).
% :param frequency: The operating frequency (Hz).
% :param target_rcs: The target radar cross section (m^2).
% :return: The power at the radar (W).
%
% Created by: Lee A. Harrison
% On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Calculate the wavelength
wavelength = 299792458 / frequency;

% Calculate the power at the radar
pr = (peak_power * antenna_gain ^ 2 * wavelength ^ 2 * target_rcs) ./ ((4.0 * pi) ^ 3 * target_range .^ 4);

end