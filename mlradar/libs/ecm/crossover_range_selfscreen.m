function cr = crossover_range_selfscreen(peak_power, antenna_gain, ...
    target_rcs, jammer_bandwidth, effective_radiated_power, radar_bandwidth, losses)
%% Calculate the crossover range for a self screening jammer.
%     :param peak_power: The peak transmitted power of the radar (W).
%     :param antenna_gain: The gain of the radar antenna.
%     :param target_rcs: The target radar cross section (m^2).
%     :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
%     :param effective_radiated_power: The jammer's effective radiated power (W).
%     :param radar_bandwidth: The radar receiver bandwidth (Hz).
%     :param losses: The radar losses.
%     :return: The crossover range (m).
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

% Calculate the crossover range
cr = sqrt((peak_power * antenna_gain * target_rcs * jammer_bandwidth) ./...
        (effective_radiated_power * 4.0 * pi * radar_bandwidth * losses));
