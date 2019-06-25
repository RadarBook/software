function [ rcs_tm, rcs_te ] = rectangular_plate(frequency, width, length, incident_theta, observation_theta, observation_phi)
%% Calculate the bistatic radar cross section for a rectangular plate.
%     :param frequency: The frequency of the incident energy (Hz).
%     :param width: The width of the plate (m).
%     :param length: The length of the plate (m).
%     :param incident_theta: The incident angle theta (deg).
%     :param observation_theta: The observation angle theta (deg).
%     :param observation_phi: The observation angle phi (deg).
%     :return: The bistatic radar cross section (m^2).

%     Created by: Lee A. Harrison
%     On: 1/17/2019

% Speed of light
c = 299792458;

% Wavelength
wavelength = c / frequency;

theta_i = pi / 180 * incident_theta;
theta_o = pi / 180 * observation_theta;

phi_o = pi / 180 * observation_phi;

x = width / wavelength * sin(theta_o) * cos(phi_o);
y = length / wavelength * (sin(theta_o) * sin(phi_o) - sin(theta_i));

rcs_tm = 4.0 * pi * (length * width / wavelength) ^ 2 * (cos(theta_i) ^ 2 * (cos(theta_o) ^ 2 * cos(phi_o) ^ 2 + sin(phi_o) ^ 2)) * sinc(x) ^ 2 * sinc(y) ^ 2;

rcs_te = 4.0 * pi * (length * width / wavelength) ^ 2 * (cos(theta_o) ^ 2 * sin(phi_o) ^ 2 + cos(phi_o) ^ 2) * sinc(x) ^ 2 * sinc(y) ^ 2;