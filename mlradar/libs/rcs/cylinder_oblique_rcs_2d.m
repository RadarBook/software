function [ rcs_te, rcs_tm ] = cylinder_oblique_rcs_2d(frequency, radius, incident_angle, observation_angle, number_of_modes)
%% Calculate the bistatic radar cross section for the infinite cylinder with oblique incidence.
%     :param frequency: The frequency of the incident energy (Hz).
%     :param radius: The radius of the cylinder (m).
%     :param incident_angle: The angle of incidence from z-axis (deg).
%     :param observation_angle: The observation angle (deg).
%     :param number_of_modes: The number of terms to take in the summation.
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

% Wavenumber
k = 2.0 * pi / wavelength;

% Initialize the sum
s_tm = 0;
s_te = 0;

phi = observation_angle * pi / 180;
theta_i = incident_angle * pi / 180;

% Argument for Bessel and Hankel functions
z = k * radius * sin(theta_i);

for n = 0:(number_of_modes + 1)
    en = 2.0;
    if n == 0
        en = 1.0;
    end
    
    an = besselj(n, z) / besselh(n, 2, z);
    
    jp = n * besselj(n, z) / z - besselj(n + 1, z);
    hp = n * besselh(n, 2, z) / z - besselh(n + 1, 2, z);
    
    bn = -jp / hp;
    
    s_tm = s_tm + en * an * cos(n * phi);
    s_te = s_te + en * bn * cos(n * phi);
end

rcs_tm = 2.0 * wavelength / (pi * sin(theta_i)) * abs(s_tm) ^ 2;
rcs_te = 2.0 * wavelength / (pi * sin(theta_i)) * abs(s_te) ^ 2;