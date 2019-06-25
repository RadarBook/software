function [ rcs_te, rcs_tm ] = cylinder_oblique_rcs_3d(frequency, radius, incident_angle, observation_angle, number_of_modes, length)
%% Calculate the bistatic radar cross section for a finite length cylinder with oblique incidence.
%     :param frequency: The frequency of the incident energy (Hz).
%     :param radius: The radius of the cylinder (m).
%     :param incident_angle: The angle of incidence from z-axis (deg).
%     :param observation_angle: The observation angle (deg).
%     :param number_of_modes: The number of terms to take in the summation.
%     :param length: The length of the cylinder (m).
%     :return: The bistatic radar cross section for the infinite cylinder (m^2).

%     Created by: Lee A. Harrison
%     On: 1/15/2019

% Speed of light
c = 299792458;

% Wavelength
wavelength = c / frequency;

theta_i = incident_angle * pi / 180;
theta_o = theta_i;

% Calculate the 2D RCS
[rcs_te, rcs_tm] = cylinder_oblique_rcs_2d(frequency, radius, incident_angle, observation_angle, number_of_modes);

% Scale factor
value = 2.0 * length ^ 2 / wavelength * sin(theta_o) ^ 2 * sinc(length / wavelength * (cos(theta_i) + cos(theta_o))) ^ 2;

% Scale the values
rcs_te = rcs_te * value;
rcs_tm = rcs_tm * value;