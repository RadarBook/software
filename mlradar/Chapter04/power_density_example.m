%% Power density example
% Created by: Lee A. Harrison
% On: 7/2/2018

clear, clc

% Peak transmit power (W)
peak_power = 50e3;

% Antenna gain (dB)
antenna_gain = 20;

% Target range (m)
target_range = linspace(1e3, 5e3, 1000);

% Calculate the power density (W/m^2)
pd = power_density_radar(peak_power, lin(antenna_gain), target_range);

% Plot the result
figure;
plot(target_range/1e3, pd);
title('Incident Power Density');
xlabel('Target Range (km)');
ylabel('Power Density (W/m^{2})');
grid on;
plot_settings;

