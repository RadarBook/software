%% Vegetation attenuation example
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Specific attenuation (dB/m)
specific_attenuation = 0.39;

% Maximum attenuation (dB)
maximum_attenuation = 34.10;

% Distance (m)
distance = linspace(0, 100.0);

% Calculate the attenuation due to vegetation
attenuation = maximum_attenuation * (1. - exp(-distance * specific_attenuation / maximum_attenuation));

% Plot the results
figure;
semilogy(distance, attenuation);
title('Vegetation Attenuation');
xlabel('Distance (m)');
ylabel('Attenuation (dB)');
grid on; plot_settings;