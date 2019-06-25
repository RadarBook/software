function snr = output_snr_polar(peak_power, transmit_antenna_gain, receive_antenna_gain, r, theta, separation_distance,...
    frequency, bistatic_target_rcs, system_temperature, bandwidth, noise_factor, transmit_losses, receive_losses)
%% Calculate the bistatic output signal to noise ratio.
%     :param peak_power: The peak transmitted power (W).
%     :param transmit_antenna_gain: The gain of the transmitting antenna.
%     :param receive_antenna_gain: The gain of the receiving antenna.
%     :param r: The range from the origin to the target (m).
%     :param theta: The angle from the "x" axis to the target (rad).
%     :param separation_distance: The distance from the transmitter to the receiver (m).
%     :param frequency: The operating frequency (Hz).
%     :param bistatic_target_rcs: The target bistatic radar cross section (m^2).
%     :param system_temperature: The system temperature (K).
%     :param bandwidth: The operating bandwidth (Hz).
%     :param noise_factor: The receiver noise factor.
%     :param transmit_losses: The loss in the transmitter.
%     :param receive_losses: THe loss in the receiver.
%     :return: The output signal to noise ratio for bistatic configurations.
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018

% Speed of light
c = 299792458;

% Boltzmann's constant
k = 1.38064852e-23;

% Calculate the wavelength
wavelength = c / frequency;

% Calculate the range product
range_product = (r.^2 + (0.5 * separation_distance)^2).^2 - (r * separation_distance .* cos(theta)).^2;

% Calculate the output signal to noise ratio
snr = (peak_power * transmit_antenna_gain * receive_antenna_gain * bistatic_target_rcs * wavelength .^ 2) ./ ...
    ((4.0 * pi) ^ 3 * k * system_temperature * bandwidth * noise_factor * transmit_losses * receive_losses * range_product);