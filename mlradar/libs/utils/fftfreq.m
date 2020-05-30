function [ frequencies ] = fftfreq( n, dt )
%% Helper function similar to SciPy
%   :param n: The number of elements in the array.
%   :param dt: The time step in the array.
%   :return: The corresponding frequency array.
%
% Created by: Lee A. Harrison
% On: 4/27/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Maximum frequency (+/-)
f_max = 1.0 / (2.0 * dt);

% Frequency step
df = 1.0 / (n * dt);

% Calculate the frequencies
f_space = linspace(0, 2.0 * f_max - df, n);

frequencies = mod(f_space + f_max, 2.0 * f_max) - f_max;