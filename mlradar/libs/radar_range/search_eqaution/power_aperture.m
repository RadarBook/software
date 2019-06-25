function pa = power_aperture(system_temperature, noise_factor, losses, signal_to_noise, target_range, search_volume, scan_time, target_rcs)
%% Calculate the power aperture product.
%     :param system_temperature: The system temperature (K).
%     :param noise_factor: The receiver noise factor.
%     :param losses: The system losses.
%     :param signal_to_noise: The signal to noise ratio.
%     :param target_range: The target distance from the transmitting antenna (m).
%     :param search_volume: The volume to search (steradians).
%     :param scan_time: The time to scan the volume (s).
%     :param target_rcs: The target radar cross section (m^2).
%     :return: The power aperture product (dB).
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018

% Boltzmann's constant
k = 1.38064852e-23;

% Calculate the power aperture
pa = signal_to_noise * (4.0 * pi * k * system_temperature * noise_factor * losses * target_range .^ 4 * search_volume) ./ (target_rcs * scan_time);