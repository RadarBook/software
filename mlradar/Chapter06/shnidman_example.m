%% Shnidman example
% Created by: Lee A. Harrison
% On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
pd = linspace(0.1, 0.99, 200);
pfa = 1.0e-6;
number_of_pulses = 10;
target_type = 'Swerling 4';

% Calculate the error in the Shnidman approximation of signal to noise
error = zeros(1, length(pd));
for i = 1:length(pd)
    error(i) = 10 * log10(single_pulse_snr_swerling(pd(i), pfa, number_of_pulses, target_type)) - ...
        shnidman(pd(i), pfa, number_of_pulses, target_type);
end

% Plot the results
figure;
plot(pd, error);
ylim([-1, 1])
title('Shnidman''s Approximation');
xlabel('Probability of Detection');
ylabel('Signal to Noise Error (dB)');
grid on;
plot_settings;