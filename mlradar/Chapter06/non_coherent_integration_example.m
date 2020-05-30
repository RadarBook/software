%% Non-Coherent integration example
% Created by: Lee A. Harrison
% On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
snr_db = linspace(-4.0, 18.0);
snr = 10.^(snr_db/10);
pfa = 1.0e-9;
number_of_pulses = 10;
target_type = 'Swerling 0';

% Calculate the probability of detection
pd = non_coherent_integration(snr, pfa, number_of_pulses, target_type);

% Plot the results
figure;
plot(snr_db, pd);
title('Noncoherent Integration');
xlabel('Signal to Noise (dB)');
ylabel('Probability of Detection');
grid on;
plot_settings;