function [ signal ] = chirp(t, start_frequency, t1, end_frequency)
%% Generate a chirp waveform
%   :param t: The time array (s).
%   :param start_frequency: The starting frequency of the chirp (Hz).
%   :param t1: The time at which the end frequency is specified (s).
%   :param end_frequency: The ending frequency of the chirp (Hz).
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

f = start_frequency + 0.5 * (end_frequency - start_frequency) * t / t1;

signal = cos(2.0 * pi * f .* t);

end