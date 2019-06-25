function [ rcs ] = rcs_frustum( frequency, nose_radius, base_radius, length, incident_angle )
%% Calculate the radar cross section of a frustum.
%     :param frequency: The operating frequency (Hz).
%     :param nose_radius: The radius of the nose (m).
%     :param base_radius: The radius of the base (m).
%     :param length: The length (m).
%     :param incident_angle: The incident angle (rad).
%     :return: The radar cross section of the frustum (m^2).

%     Created by: Lee A. Harrison
%     On: 1/15/2019

% Speed of light
c = 299792458;

% Wavelength
wavelength = c / frequency;

% Wavenumber
k = 2.0 * pi / wavelength;

% Calculate the half cone angle
half_cone_angle = atan((base_radius - nose_radius) / length);

% Calculate the heights
z2 = base_radius * tan(half_cone_angle);
z1 = nose_radius * tan(half_cone_angle);

% Calculate the RCS
if abs(incident_angle - (0.5 * pi + half_cone_angle)) < 1e-12;
    % Specular
    rcs = 8.0 / 9.0 * pi * (z2 ^ 1.5 - z1 ^ 1.5) ^ 2 * sin(half_cone_angle) / (wavelength * cos(half_cone_angle) ^ 4);
elseif incident_angle < 1e-3
    % Base
        rcs = wavelength ^ 2 * (k * base_radius) ^ 4 / (4.0 * pi);
elseif pi - incident_angle < 1e-3
    % Nose
        rcs = wavelength ^ 2 * (k * nose_radius) ^ 4 / (4.0 * pi);
else
        rcs = wavelength * base_radius / (8.0 * pi * sin(incident_angle)) * (tan(incident_angle - half_cone_angle)) ^ 2;
end