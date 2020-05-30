%% Beam spreading example
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Elevation angle (degrees)
elevation_angle = 5;  

% Target height (km)
height = 5; 

% Set up the elevation and height arrays
[theta, height] = meshgrid(linspace(0.0, elevation_angle, 200), linspace(0.0, height, 200));

% Calculate the beam spreading loss
b = 1. - (0.5411 + 0.07446 * theta + (0.06272 + 0.0276 * theta) .* height + 0.008288 .* height .^ 2) ./ ...
    (1.728 + 0.5411 .* theta + (0.1815 + 0.06272 .* theta + 0.0138 .* theta .^ 2) .* height + ...
    (0.01727 + 0.008288 .* theta) .* height .^ 2) .^ 2;

beam_spreading_loss = -db(b);

% Plot the results as a color plot
figure; 
pcolor(theta, height, beam_spreading_loss); shading flat;
title('Beam Spreading Loss')
xlabel('Elevation Angle (degrees)')
ylabel('Height (km)');
colormap('jet'); colorbar; plot_settings;