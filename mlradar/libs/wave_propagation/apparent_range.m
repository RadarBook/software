function range = apparent_range(radar_lla, target_lla)
%% Calculate the apparent range due to refraction.
% :param radar_lla: The radar location in LLA (deg, deg, m).
% :param target_lla: The target location in LLA (deg, deg, m).
% :return: The apparent range from the radar to the target (meters).
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Convert the radar and target locations
[x,y,z]  = lla_to_ecef(radar_lla(1) * pi/180, radar_lla(2) * pi/180, radar_lla(3));
radar_ecef(1) = x; radar_ecef(2) = y; radar_ecef(3) = z;

[x,y,z] = lla_to_ecef(target_lla(1) * pi/180, target_lla(2) * pi/180, target_lla(3));
target_ecef(1) = x; target_ecef(2) = y; target_ecef(3) = z;

% Standard values
a = 0.000315;
b = 0.1361;

% Find the vector from the radar to the target
line_of_sight = target_ecef - radar_ecef;

% Divide the line of sight into many points for the summation
number_of_points = 1000;

delta = line_of_sight / (number_of_points - 1);

% Loop over all the points and perform the summation to find the additional length
s = 0;

for i = 1:number_of_points
    % Find the altitude of each point
    l = radar_ecef + delta * (i - 1);
    [~, ~, alt] = ecef_to_lla(l(1), l(2), l(3));
    s = s + ((1. + a * exp(-b * alt / 1.e3)) - 1.) * norm(delta);
end

range.true = norm(line_of_sight);
range.apparent = s + norm(line_of_sight);