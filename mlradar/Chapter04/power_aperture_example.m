%% Power aperture example
% Created by: Lee A. Harrison
% On: 7/2/2018

clear, clc

% Target range (m)
target_range = linspace(1e3, 100e3, 1000);

% System temperature (K)
system_temperature = 290;

% Search volume (steradian)
search_volume = 400;

% Noise figure (dB)
noise_figure = 6;

% Losses (dB)
losses = 4;

% Signal to noise ratio (dB)
signal_to_noise = 20;

% Scan time (s)
scan_time = 2;

% Target radar cross section (dBsm)
target_rcs = 10;

% Calculate the power aperture
pa = power_aperture(system_temperature, lin(noise_figure), lin(losses),...
    lin(signal_to_noise), target_range, search_volume, scan_time, lin(target_rcs));

% Plot the result
figure;
plot(target_range/1e3, db(pa));
title('Power Aperture Product');
xlabel('Target Range (km)');
ylabel('Power Aperture (dB)');
grid on;
plot_settings;