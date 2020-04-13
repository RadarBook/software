function [ js ] = jammer_to_signal(peak_power, antenna_gain, target_rcs, ...
                    jammer_range, jammer_bandwidth, jammer_erp, target_range, ...
                    radar_bandwidth, losses, antenna_gain_jammer_direction)
%% Calculate the jammer to signal ratio.
%     :param peak_power: The peak transmitted power of the radar (W).
%     :param antenna_gain: The gain of the radar antenna.
%     :param target_rcs: The target radar cross section (m^2).
%     :param jammer_range: The range from the radar to the jammer (m).
%     :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
%     :param jammer_erp: The jammer's effective radiated power (W).
%     :param target_range: The range to the target (m).
%     :param radar_bandwidth: The radar receiver bandwidth (Hz).
%     :param losses: The radar losses.
%     :param antenna_gain_jammer_direction: The gain of the radar antenna in the direction of the jammer.
%     :return: The signal to jammer ratio.
%
%     Created by: Lee A. Harrison
%     On: 5/25/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Check the bandwidth
if jammer_bandwidth > radar_bandwidth
        jammer_bandwidth = radar_bandwidth;
end

js = (jammer_erp * 4.0 * pi * target_range .^ 4 * radar_bandwidth * losses ...
    * antenna_gain_jammer_direction)./ (peak_power * antenna_gain .^ 2 * ...
    target_rcs * jammer_bandwidth * jammer_range .^ 2);