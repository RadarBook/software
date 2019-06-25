function r_max = maximum_range(system_temperature, bandwidth, noise_factor, losses, signal_to_noise, peak_power, antenna_gain, frequency, target_rcs)
%% Calculate the maximum range that the radar can detect the target.
%     :param system_temperature: The system temperature (K).
%     :param bandwidth: The operating bandwidth (Hz).
%     :param noise_factor: The receiver noise factor.
%     :param losses: The system losses.
%     :param signal_to_noise: The operating signal to noise ratio.
%     :param peak_power: The peak transmitted power (W).
%     :param antenna_gain: The gain of the transmitting antenna.
%     :param frequency: The operating frequency (Hz).
%     :param target_rcs: The target radar cross section (m^2).
%     :return: The maximum range at which a target can be detected (m).
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018

% First, calculate the minimum detectable signal
min_signal = minimum_detectable_signal(system_temperature, bandwidth, noise_factor, losses, signal_to_noise);

% Calculate the maximum detection range
r_max = ((peak_power * antenna_gain ^ 2 * (299792458 / frequency) ^ 2 * target_rcs) ./ ((4.0 * pi) ^ 3 * min_signal)) .^ 0.25;