function br = burn_through_range_escort(peak_power, antenna_gain, target_rcs, radar_bandwidth, losses, jammer_range,...
                       jammer_to_signal_req, effective_radiated_power, jammer_bandwidth, antenna_gain_jammer_direction)
%% Calculate the burn through range for escort jamming.
%     :param peak_power: The peak transmitted power of the radar (W).
%     :param antenna_gain: The gain of the radar antenna.
%     :param target_rcs: The target radar cross section (m^2).
%     :param radar_bandwidth: The radar receiver bandwidth (Hz).
%     :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
%     :param effective_radiated_power: The jammer's effective radiated power (W).
%     :param losses: The radar losses.
%     :param effective_radiated_power: The jammer's effective radiated power (W).
%     :param jammer_to_signal_req: The jammer to signal ratio required to perform a specific radar function.
%     :param jammer_range: The range from the radar to the jammer (m).
%     :param antenna_gain_jammer_direction: The gain of the radar antenna in the direction of the jammer.
%     :return: The burn through range (m).
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

% Calculate the burn through range
br = (jammer_to_signal_req * (peak_power * antenna_gain .^ 2 * target_rcs * jammer_range .^ 2 * jammer_bandwidth)./...
          (effective_radiated_power * antenna_gain_jammer_direction * 4.0 * pi * radar_bandwidth * losses)) .^ 0.25;
