%% Loop gain example
% Created by: Lee A. Harrison
% On: 7/1/2018

clear, clc

% Reference range (m)
reference_range = 100e3;

% Reference radar cross section (dBsm)
reference_rcs = 10;

% Reference signal to noise ratio (dB)
reference_snr = 20.0;

% Calculate the loop gain
lg = loop_gain(reference_range, 10^(reference_rcs/10), 10^(reference_snr/10));

% Display the result
fprintf('Loop gain = %.2f (dB)\n', db(lg));