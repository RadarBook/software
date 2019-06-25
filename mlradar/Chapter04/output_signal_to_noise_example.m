%% Output signal to noise example
% Created by: Lee A. Harrison
% On: 7/1/2018

clear, clc

% Peak transmit power (W)
peak_power = 50e3;

% Antenna gain (dB)
antenna_gain = 20;

% Target range (m)
target_range = linspace(1e3, 100e3, 1e3);

% Operating frequency (Hz)
frequency = 1.0e9;

% Target radar cross section (dBsm)
target_rcs = 10;

% System temperature (K)
system_temperature = 290;

% Receiver bandwidth (Hz)
bandwidth = 10e6;

% Noise figure (dB)
noise_figure = 6;

% Losses (dB)
losses = 4;

% Calculate the output signal to noise ratio
snr = output_snr(system_temperature, bandwidth, lin(noise_figure), lin(losses), ...
    peak_power, lin(antenna_gain), frequency, lin(target_rcs), target_range);

% Plot the result
figure;
plot(target_range/1e3, db(snr));
title('Output Signal to Noise Ratio');
xlabel('Target Range (km)');
ylabel('Output Signal to Noise Ratio (dB)');
grid on;
plot_settings;