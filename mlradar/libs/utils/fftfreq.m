function [ frequencies ] = fftfreq( n, dt )
%% Helper function similar to SciPy
%   :param n: The number of elements in the array.
%   :param dt: The time step in the array.
%   :return: The corresponding frequency array.
%
% Created by: Lee A. Harrison
% On: 4/27/2019

% Maximum frequency (+/-)
f_max = 1.0 / (2.0 * dt);

% Frequency step
df = 1.0 / (n * dt);

% Calculate the frequencies
f_space = linspace(0, 2.0 * f_max - df, n);

frequencies = mod(f_space + f_max, 2.0 * f_max) - f_max;