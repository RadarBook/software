%% Frustum example
% Created by: Lee A. Harrison
% On: 1/15/2019

clear, clc

% Set the parameters
frequency = 1.0e9;  % Hz
nose_radius = 0.1; % meters
base_radius = 0.2; % meters
length = 0.8; % meters

% Set the incident angles
incident_angle = linspace(0, pi, 1801);

% Calculate the radar cross section
for i = 1:numel(incident_angle)
    rcs(i) = rcs_frustum(frequency, nose_radius, base_radius, length, incident_angle(i));
end

% Display the results
figure;
plot(incident_angle * 180 / pi, 10 * log10(rcs))
title('RCS vs Incident Angle')
ylabel('RCS (dBsm)')
xlabel('Incident Angle (deg)')

% Turn on the grid
grid on

% Plot settings
plot_settings;