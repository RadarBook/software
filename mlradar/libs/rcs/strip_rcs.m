function [ rcs_te, rcs_tm ] = strip_rcs(frequency, width, incident_angle, observation_angle)
%% Calculate the bistatic radar cross section for a 2D strip.
%     :param frequency: The frequency of the incident energy (Hz).
%     :param width: The width of the strip (m).
%     :param incident_angle: The incident angle (deg).
%     :param observation_angle: The observation angle (deg).
%     :return: The bistatic radar cross section (m^2).

%     Created by: Lee A. Harrison
%     On: 1/15/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Speed of light
c = 299792458;

% Wavelength
wavelength = c / frequency;

% Wavenumber
k = 2.0 * pi / wavelength;

phi_i = incident_angle * pi / 180;

phi_o = observation_angle * pi / 180;

rcs_tm = k * width ^ 2 * sin(phi_i) * sinc(width / wavelength * (cos(phi_o) + cos(phi_i))) ^ 2;

rcs_te = k * width ^ 2 * sin(phi_o) * sinc(width / wavelength * (cos(phi_o) + cos(phi_i))) ^ 2;