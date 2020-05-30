%% Resolution example
% Created by: Lee A. Harrison
% On: 9/19/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
number_of_bits = 12;
signal_to_noise = 68.0;

% Calculate the ideal signal to noise
fprintf('Ideal SNR = %.2f (dB)\n', 6.02 * number_of_bits + 1.76);

% Calculate the effective number of bits
fprintf('Effective Number of Bits %d\n', round((signal_to_noise - 1.76) / 6.02));
