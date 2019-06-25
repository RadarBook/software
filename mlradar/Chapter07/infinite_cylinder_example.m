%% Infinite cylinder example
% Created by: Lee A. Harrison
% On: 1/15/2019

clear, clc

% Set the parameters
frequency = 300e6; % Hz
radius = 3; % meters
length = 20; % meters
number_of_modes = 60;

% 2D or 3D RCS
mode = '2D';

% Set the observation angles
observation_angle = linspace(-90, 90, 1801);

if strcmp(mode, '2D')
    for i = 1:numel(observation_angle)
        [rcs_te(i), rcs_tm(i)] = cylinder_rcs_2d(frequency, radius, observation_angle(i), number_of_modes);
    end
else
    for i = 1:numel(observation_angle)
        [rcs_te(i), rcs_tm(i)] = cylinder_rcs_3d(frequency, radius, observation_angle(i), number_of_modes, length);
    end
end

% Display the results
figure;
plot(observation_angle, 10.0 * log10(rcs_te)); hold on;
plot(observation_angle, 10.0 * log10(rcs_tm), '--')

% Set the plot title and labels
title('RCS vs Bistatic Angle')
ylabel('RCS (dBsm)')
xlabel('Observation Angle (deg)')
ylim([min(10.0 * log10(rcs_te)) - 3, max(10.0 * log10(rcs_te)) + 3])

% Set the legend
legend({'TE^{z}', 'TM^{z}'})

% Turn on the grid
grid on

% Plot settings
plot_settings;
