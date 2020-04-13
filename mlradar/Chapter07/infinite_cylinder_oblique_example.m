%% Infinite cylinder oblique example
% Created by: Lee A. Harrison
% On: 1/15/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
frequency = 300e6; % Hz
radius = 3; % meters
length = 20; % meters
incident_angle = 50; % degrees
number_of_modes = 60;

% 2D or 3D RCS
mode = '3D';

% Set the observation angles
observation_angle = linspace(-90, 90, 1801);

if strcmp(mode, '2D')
    for i = 1:numel(observation_angle)
        [rcs_te(i), rcs_tm(i)] = cylinder_oblique_rcs_2d(frequency, radius, incident_angle, observation_angle(i), number_of_modes);
    end
else
    for i = 1:numel(observation_angle)
        [rcs_te(i), rcs_tm(i)] = cylinder_oblique_rcs_3d(frequency, radius, incident_angle, observation_angle(i), number_of_modes, length);  
    end
end

% Display the results
figure;
plot(observation_angle, 10.0 * log10(rcs_te + 1e-10)); hold on;
plot(observation_angle, 10.0 * log10(rcs_tm + 1e-10), '--')

% Set the plot title and labels
title('RCS vs Bistatic Angle')
ylabel('RCS (dBsm)')
xlabel('Observation Angle (deg)')
ylim([min(10.0 * log10(rcs_te + 1e-10)) - 3, max(10.0 * log10(rcs_te + 1e-10)) + 3])

% Set the legend
legend({'TE^{z}', 'TM^{z}'})

% Turn on the grid
grid on

% Plot settings
plot_settings;
