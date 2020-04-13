%% Rectangular plate example
% Created by: Lee A. Harrison
% On: 1/17/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
frequency = 300e6;  % Hz
width = 3; % meters
length = 5; % meters
incident_theta = 15.0; % degrees

% Set the observation angles
observation_phi = 90.0; % degrees
observation_theta = linspace(-90, 90, 1801); % degrees

% Calculate the radar cross section
for i = 1:numel(observation_theta)
    [rcs_tm(i), rcs_te(i)] = rectangular_plate(frequency, width, length, incident_theta, observation_theta(i), observation_phi);
end

% Display the results
figure;
plot(observation_theta, 10 * log10(rcs_te)); hold on;
plot(observation_theta, 10 * log10(rcs_tm), '--')
title('RCS vs Observation Angle')
ylabel('RCS (dBsm)')
xlabel('Observation Angle (deg)')

ylim([min(10 * log10(rcs_te + 1e-4)) - 3, max(10 * log10(rcs_te + 1e-4)) + 3])

% Legend
legend({'TE^{x}', 'TM^{x}'})

% Turn on the grid
grid on

% Plot settings
plot_settings;