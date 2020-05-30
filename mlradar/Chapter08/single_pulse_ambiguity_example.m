%% Single pulse ambiguity example
% Created by: Lee A. Harrison
% On: 4/27/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
pulsewidth = 1e-3; % seconds

%% Zero Doppler cut

% Set the time delay
time_delay = linspace(-pulsewidth, pulsewidth, 5000);

% Calculate the ambiguity function
ambiguity = single_pulse(time_delay, eps, pulsewidth);

figure;
plot(time_delay, ambiguity);
xlabel('Time (s)');
ylabel('Relative Amplitude');
title('Unmodulated Pulse Ambiguity Function');
grid on;
plot_settings;

%% Zero range cut

% Set the Doppler mismatch
doppler_frequency = linspace(-2.0 / pulsewidth, 2.0 / pulsewidth, 5000);

% Calculate the ambiguity function
ambiguity = single_pulse(eps, doppler_frequency, pulsewidth);

figure;
plot(doppler_frequency, ambiguity);
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('Unmodulated Pulse Ambiguity Function');
grid on;
plot_settings;

%% 2D contour

% Set the time delay
time_delay = linspace(-pulsewidth, pulsewidth, 500);

% Set the Doppler mismatch
doppler_frequency = linspace(-2.0 / pulsewidth, 2.0 / pulsewidth, 500);

% Create the grid
[t, f] = meshgrid(time_delay, doppler_frequency);

% Calculate the ambiguity function
ambiguity = single_pulse(t, f, pulsewidth);

figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('Unmodulated Pulse Ambiguity Function');
grid on;
plot_settings;