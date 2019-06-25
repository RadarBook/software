%% Rain attenuation example
% Created by: Lee A. Harrison
% On: 6/18/2018

clear, clc

% Operating frequency (GHz)
frequency = linspace(1.0, 1000);

% Rain rate (mm/hr)
rain_rate = 5.0;

% Elevation angle (deg)
elevation_angle = 10.0;

% Polarization tilt angle (deg)
polarization_tilt_angle = 0;

% Calculate the rain attenuation
attenuation = rain_attenuation(frequency, rain_rate, elevation_angle, polarization_tilt_angle);

% Plot the results
figure;
plot(frequency, attenuation);
title('Rain Attenuation');
xlabel('Frequency (GHz)');
ylabel('Specific Attenuation (dB/km)');
grid on; plot_settings;