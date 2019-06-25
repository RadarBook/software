function [lat, lon, alt] = ecef_to_lla(ecef_x, ecef_y, ecef_z)
%% Convert coordinates in ECEF to LLA.
% :param ecef_x: The x coordinate of the point (meters).
% :param ecef_y: The y coordinate of the point (meters).
% :param ecef_z: The z coordinate of the point (meters).
% :return: The LLA coordinates of the point.
%
% Created by: Lee A. Harrison
% On: 6/18/2018

%% Earth constants
effective_earth_radius = 6378137;
earth_eccentricity = 8.1819190842622e-2;

%% Effective polar radius
earth_radius_polar = sqrt(effective_earth_radius^2 * (1. - earth_eccentricity^2));

ep = sqrt((effective_earth_radius^2 - earth_radius_polar^2) / earth_radius_polar^2);

%% Radius in xy plane
r = sqrt(ecef_x * ecef_x + ecef_y * ecef_y);

%% Angle from the xy plane
theta = atan2(effective_earth_radius * ecef_z, earth_radius_polar * r);

%% Calculate the coordinates
lat = atan2((ecef_z + ep^2 * earth_radius_polar * sin(theta)^3), (r - earth_eccentricity^2 * effective_earth_radius * cos(theta)^3));

lon = mod(atan2(ecef_y, ecef_x), 2. * pi);

alt = r / cos(lat) - effective_earth_radius / sqrt(1. - earth_eccentricity^2 * sin(lat)^2);