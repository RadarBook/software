%% Apparent range example
% Created by: Lee A. Harrison
% On: 6/18/2018

clear, clc

% Radar LLA coordinates
radar_lla = [34.0, 84.0, 120.0];

% Target LLA coordinates
target_lla = [34.0, 80.0, 12000.0];

% Apparent range
range = apparent_range(radar_lla, target_lla);

% Display the true and apparent ranges
display(sprintf('True range = %.2f (km) \nApparent range = %.2f (km)', range.true/1e3, range.apparent/1e3));