%% Maximum detection range example
% Created by: Lee A. Harrison
% On: 7/1/2018

clear, clc

% System temperature (K)
system_temperature = 290;

% Receiver bandwidth (Hz)
bandwidth = 10e6;

% Noise figure (dB)
noise_figure = 6;

% System losses (dB)
losses = 4;

% Signal to noise ratio (dB)
signal_to_noise = linspace(5, 25, 1000);

% Peak transmit power (W)
peak_power = 50e3;

% Antenna gain (dB)
antenna_gain = 20;

% Operating frequency (Hz)
frequency = 1e9;

% Target radar cross section (dBsm)
target_rcs = 10;

% Calculate the maximum detection range (m)
r_max = maximum_range(system_temperature, bandwidth, lin(noise_figure), lin(losses), ...
    lin(signal_to_noise), peak_power, lin(antenna_gain), frequency, lin(target_rcs));

% Plot the result
figure;
plot(signal_to_noise, r_max/1e3);
title('Maximum Detection Range');
xlabel('Signal to Noise Ratio (dB)');
ylabel('Detection Range (km)');
grid on;
plot_settings;
