%% Noise figure example
% Created by: Lee A. Harrison
% On: 9/19/2018

clear, clc

% Set the parameters
gain = [20, -0.5, -6, -1, 30];
noise_figure = [3.0, 0.5, 6, 1, 5];

% Calculate the total noise figure
total_noise_figure = cascade_noise_figure(gain, noise_figure);

% Display
fprintf('Total noise figure = %.2f\n', total_noise_figure);