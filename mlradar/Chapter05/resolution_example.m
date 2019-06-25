%% Resolution example
% Created by: Lee A. Harrison
% On: 9/19/2018

clear, clc

% Set the parameters
number_of_bits = 12;
signal_to_noise = 68.0;

% Calculate the ideal signal to noise
fprintf('Ideal SNR = %.2f (dB)\n', 6.02 * number_of_bits + 1.76);

% Calculate the effective number of bits
fprintf('Effective Number of Bits %d\n', round((signal_to_noise - 1.76) / 6.02));
