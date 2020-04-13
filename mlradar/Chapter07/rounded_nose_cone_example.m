%% Rounded nose cone example
% Created by: Lee A. Harrison
% On: 1/18/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
frequency = 1e9; % Hz
cone_half_angle = 20; % degrees
nose_radius = 1.4; % meters

% Set the incident angles
incident_angle = linspace(0, cone_half_angle * pi / 180, 1801);

% Calculate the radar cross section
for i = 1:numel(incident_angle)
    rcs(i) = abs(rounded_nose_cone(frequency, cone_half_angle * pi / 180, nose_radius, incident_angle(i)));
end

% Display the results
figure;
plot(incident_angle, 10 * log10(rcs));
title('RCS vs Incident Angle')
ylabel('RCS (dBsm)')
xlabel('Incident Angle (deg)')

ylim([min(10 * log10(rcs + 1e-4)) - 3, max(10 * log10(rcs + 1e-4)) + 3])

% Turn on the grid
grid on

% Plot settings
plot_settings;