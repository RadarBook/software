%% Power at radar bistatic example
% Created by: Lee A. Harrison
% On: 7/2/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Peak transmit power (W)
peak_power = 50e3;

% Transmit antenna gain (dB)
transmit_antenna_gain = 20;

% Receive antenna gain (dB)
receive_antenna_gain = 10;

% Transmit/Receive range product (m^2)
range_product = linspace(1e3, 100e3, 1000);

% Operating frequency (Hz)
frequency = 1.0e9;

% Bistatic target radar cross section (dBsm)
bistatic_target_rcs = 10;

% Calculate the power at the receiver (W)
pr = power_at_radar_bistatic(peak_power, lin(transmit_antenna_gain),...
    lin(receive_antenna_gain), 1.0, range_product,...
    frequency, lin(bistatic_target_rcs));

% Plot the result
figure;
plot(range_product/1e6, pr);
title('Bistatic Power at the Receiver');
xlabel('Range Product (km^{2})');
ylabel('Power at the Receiver (W)');
grid on;
plot_settings;