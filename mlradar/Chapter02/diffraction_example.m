%% Diffraction loss example
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Operating frequency (Hz)
frequency = linspace(1e6, 300e6, 500);

% Relative permittivity
relative_permittivity = 1.3;

% Conductivity (S/m)
conductivity = 0.01;

% Radar LLA (deg, deg, m)
radar.lat = 26.5;
radar.lon = 97.0;
radar.alt = 1000.0;

% Target LLA (deg, deg, m)
target.lat = 31.0;
target.lon = 96.0;
target.alt = 13000.0;

% Calculate the diffraction loss
diffraction_loss = diffraction_attenuation(radar, target, frequency, relative_permittivity, conductivity);

% Plot the results
figure;
plot(frequency, diffraction_loss);
title('Diffraction Loss')
xlabel('Frequency (Hz)')
ylabel('Diffraction Loss (dB)')
grid on; plot_settings;