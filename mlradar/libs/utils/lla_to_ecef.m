function [ecef_x, ecef_y, ecef_z] = lla_to_ecef(lat, lon, alt)

%% Convert coordinates in LLA to ECEF.
% :param lat: The latitude of the point (radians).
% :param lon: The Longitude of the point (radians).
% :param alt: The altitude of the point (meters).
% :return: The ECEF coordinates of the point (meters).
%
% Created by: Lee A. Harrison
% On: 6/18/2018

%% Earth constants
effective_earth_radius = 6378137;
earth_eccentricity = 8.1819190842622e-2;

% Radius of curvature
radius = effective_earth_radius / sqrt(1. - earth_eccentricity ^ 2 * sin(lat) ^ 2);

% Calculate the coordinates
ecef_x = (radius + alt) * cos(lat) * cos(lon);
ecef_y = (radius + alt) * cos(lat) * sin(lon);
ecef_z = ((1. - earth_eccentricity^2) * radius + alt) * sin(lat);
