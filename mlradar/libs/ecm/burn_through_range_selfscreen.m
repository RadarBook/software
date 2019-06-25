function br = burn_through_range_selfscreen(peak_power, antenna_gain, target_rcs,...
    radar_bandwidth, losses, jammer_to_signal_req, effective_radiated_power, jammer_bandwidth)
%% Calculate the burn through range for a self screening jammer.
%     :param peak_power: The peak transmitted power of the radar (W).
%     :param antenna_gain: The gain of the radar antenna.
%     :param target_rcs: The target radar cross section (m^2).
%     :param radar_bandwidth: The radar receiver bandwidth (Hz).
%     :param jammer_bandwidth: The jammer's transmitting bandwith (Hz).
%     :param effective_radiated_power: The jammer's effective radiated power (W).
%     :param losses: The radar losses.
%     :param effective_radiated_power: The jammer's effective radiated power (W).
%     :param jammer_to_signal_req: The jammer to signal required to perform a specific radar function.
%     :return: The burn through range (m).
%
%     Created by: Lee A. Harrison
%     On: 5/25/2019

% Check the bandwidth
if jammer_bandwidth > radar_bandwidth
    jammer_bandwidth = radar_bandwidth;
end

% Calculate the burn through range
br = sqrt(jammer_to_signal_req * (peak_power * antenna_gain * target_rcs * jammer_bandwidth) ./...
                (effective_radiated_power * 4.0 * pi * radar_bandwidth * losses));
