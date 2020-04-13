%% Minimum detectable signal example
% Created by: Lee A. Harrison
% On: 7/1/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% System temperature (K)
system_temperature = 290;

% Receiver bandwidth (Hz)
bandwidth = 10e6;

% Noise figure (dB)
noise_figure = 6;

% System losses (dB)
losses = 4;

% Signal to noise ration (dB)
signal_to_noise = 20;

% Calculate the minimum detectable signal (W)
p_min = minimum_detectable_signal(system_temperature, bandwidth, lin(noise_figure), lin(losses), lin(signal_to_noise));

% Display the result
fprintf('Minimum detectable signal = %.2e (W)\n', p_min);