%% Power at radar example
% Created by: Lee A. Harrison
% On: 7/2/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Peak transmit power (W)
peak_power = 50e3;

% Antenna gain (dB)
antenna_gain = 20;

% Target range (m)
target_range = linspace(1e3, 5e3, 1000);

% Operating frequency (Hz)
frequency = 1e9;

% Target radar cross section (dBsm)
target_rcs = 10;

% Calculate the power at the radar (W)
pr = power_at_radar(peak_power, lin(antenna_gain), target_range, frequency, lin(target_rcs));

% Plot the result
figure;
plot(target_range/1e3, pr);
title('Power at the Radar');
xlabel('Target Range (km)');
ylabel('Power at the Radar (W)');
grid on;
plot_settings;