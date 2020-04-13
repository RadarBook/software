%% Cloud and fog attenuation example
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Operating frequency (GHz)
frequency = linspace(1.0, 200, 256);

% Cloud/fog temperature (k)
liquid_water_temperature = 290;

% Cloud/fog density (g/m^3)
liquid_water_density = 0.5;

% Calculate the attenuation
attenuation = cloud_fog_attenuation(frequency, liquid_water_temperature, liquid_water_density);

% Plot the results
figure;
loglog(frequency, attenuation);
title('Cloud or Fog Attenuation');
xlabel('Frequency (GHz)');
ylabel('Specific Attenuation (dB/km)')
grid on; plot_settings;