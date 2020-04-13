%% Noise figure example
% Created by: Lee A. Harrison
% On: 9/19/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
gain = [20, -0.5, -6, -1, 30];
noise_figure = [3.0, 0.5, 6, 1, 5];

% Calculate the total noise figure
total_noise_figure = cascade_noise_figure(gain, noise_figure);

% Display
fprintf('Total noise figure = %.2f\n', total_noise_figure);