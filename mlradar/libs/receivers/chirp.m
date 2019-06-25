function [ signal ] = chirp(t, start_frequency, t1, end_frequency)
%% Generate a chirp waveform
%   :param t: The time array (s).
%   :param start_frequency: The starting frequency of the chirp (Hz).
%   :param t1: The time at which the end frequency is specified (s).
%   :param end_frequency: The ending frequency of the chirp (Hz).
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018

f = start_frequency + 0.5 * (end_frequency - start_frequency) * t / t1;

signal = cos(2.0 * pi * f .* t);

end