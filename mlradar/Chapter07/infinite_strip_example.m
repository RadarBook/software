%% Infinite strip example
% Created by: Lee A. Harrison
% On: 1/15/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
incident_angle = 60; % degrees
frequency = 300e6; % Hz
width = 3; % meters

% Set the observation angles
observation_angle = linspace(0, 180, 1801);

for i = 1:numel(observation_angle)
    [rcs_te(i), rcs_tm(i)] = strip_rcs(frequency, width, incident_angle, observation_angle(i));
end

% Display the results
figure;
plot(observation_angle, 10 * log10(rcs_te + 1e-10)); hold on
plot(observation_angle, 10 * log10(rcs_tm + 1e-10), '--')

% Set the plot title and labels
title('RCS vs Bistatic Angle')
ylabel('RCS (dBsm)')
xlabel('Observation Angle (deg)')
ylim([min(10 * log10(rcs_te + 1e-4)) - 3, max(10 * log10(rcs_te + 1e-4)) + 3])

% Set the legend
legend({'TE^{z}', 'TM^{z}'})

% Turn on the grid
grid on

% Plot settings
plot_settings;
