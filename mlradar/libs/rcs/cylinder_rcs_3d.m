function [ rcs_te, rcs_tm ] = cylinder_rcs_3d( frequency, radius, observation_angle, number_of_modes, length )
%% Calculate the bistatic radar cross section for a finite length cylinder.
%     :param frequency: The frequency of the incident energy (Hz).
%     :param radius: The radius of the cylinder (m).
%     :param observation_angle: The observation angle (deg).
%     :param number_of_modes: The number of terms to take in the summation.
%     :param length: The length of the cylinder (m).
%     :return: The bistatic radar cross section for the infinite cylinder (m^2).

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

% First calculate the 2D rcs
[rcs_te, rcs_tm] = cylinder_rcs_2d(frequency, radius, observation_angle, number_of_modes);

% Scaling factor
value = 2.0 * length ^ 2 / wavelength;

rcs_te = rcs_te * value;
rcs_tm = rcs_tm * value;