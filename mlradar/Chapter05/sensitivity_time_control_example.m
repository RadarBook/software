%% Sensitivity time control example
% Created by: Lee A. Harrison
% On: 9/19/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
pulse_repetition_frequency = 30e3;
pulsewidth = 1.0e-6;

% Calculate the attenuation and receive range
[receive_range, atten] = sensitivity_time_control(pulse_repetition_frequency, pulsewidth);

% Plot the results
figure;
plot(receive_range, 10.0 * log10(atten ./ max(atten)));
title('Sensitivity Time Control');
xlabel('Range (m)');
ylabel('Normalized Attenuation (dB)');
grid on;
plot_settings;