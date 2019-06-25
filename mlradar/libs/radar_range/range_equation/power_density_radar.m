function pd = power_density_radar(peak_power, antenna_gain, target_range)
%% Calculate the power density at a point in space.
% :param peak_power: The peak transmitted power (W).
% :param antenna_gain: The gain of the transmitting antenna.
% :param target_range: The target distance from the transmitting antenna (m).
% :return: The power density at the target (W/m^2).
%
% Created by: Lee A. Harrison
% On: 6/21/2018

% Calculate the power density
pd = peak_power * antenna_gain ./ (4.0 * pi * target_range .^ 2);

end