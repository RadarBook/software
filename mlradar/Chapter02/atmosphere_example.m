%% Atmospheric attenuation example
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Operating frequency (GHz)
frequency = linspace(0, 1e3, 1024);

% System temperature (K)
temperature = 290;

% Dry air pressure (hPa)
dry_air_pressure = 1013.25;

% Water vapor density (g/m^3)
water_vapor_density = 7.5;

% Get the atmospheric attenuation
attenuation = atmospheric_attenuation(frequency, temperature, dry_air_pressure, water_vapor_density);

% Plot the results
figure;
semilogy(frequency, attenuation, 'b');
title('Atmospheric Attenuation');
xlabel('Frequency (GHz)');
ylabel('Specific Attenuation (dB/km)');
grid on; plot_settings;