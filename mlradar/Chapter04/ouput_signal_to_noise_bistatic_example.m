%% Output signal to noise bistatic example
% Created by: Lee A. Harrison
% On: 7/1/2018

clear, clc

% Peak transmit power
peak_power = 50e3;

% Transmit antenna gain (dB)
transmit_antenna_gain = 20;

% Receive antenna gain (dB)
receive_antenna_gain = 10;

% Transmitter to target range (m)
transmit_target_range = 1.0;

% Receiver to target range (m)
receive_target_range = linspace(1e3, 100e3, 1e3);

% Operating frequency (Hz)
frequency = 1.0e9;

% Bistatic target radar cross section (dBsm)
bistatic_target_rcs = 10;

% System temperature (K)
system_temperature = 290;

% Receiver bandwidth (Hz)
bandwidth = 10e6;

% Noise figure (dB)
noise_figure = 6;

% Transmit losses (dB)
transmit_losses = 4;

% Receive losses (dB)
receive_losses = 2;

% Calculate the output signal to noise ratio
snr = output_snr_bistatic(peak_power, lin(transmit_antenna_gain), lin(receive_antenna_gain), transmit_target_range, receive_target_range,...
    frequency, lin(bistatic_target_rcs), system_temperature, bandwidth, lin(noise_figure), lin(transmit_losses), lin(receive_losses));

% Plot the result
figure;
plot(transmit_target_range*receive_target_range/1e6, db(snr));
title('Bistatic Radar Range Equation');
xlabel('Range Product (km^{2})');
ylabel('Output Signal to Noise Ratio (dB)');
grid on;
plot_settings;