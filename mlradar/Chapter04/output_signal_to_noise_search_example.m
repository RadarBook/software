%% Output signal to noise search example
% Created by: Lee A. Harrison
% On: 7/2/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Power aperture (W m^2)
power_aperture = 50e3;

% Search volume (steradian)
search_volume = 400;

% Scan time (s)
scan_time = 2;

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
snr = output_snr_search(power_aperture, system_temperature, lin(noise_figure), lin(losses),...
    target_range, search_volume, scan_time, lin(target_rcs));

% Plot the result
figure;
plot(target_range/1e3, db(snr));
title('Output Signal to Noise for Search');
xlabel('Target Range (km)');
ylabel('Output Signal to Noise Ratio (dB)');
grid on;
plot_settings;