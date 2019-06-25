%% Pulse train train ambiguity example
% Created by: Lee A. Harrison
% On: 4/27/2019

clear, clc

% Set the parameters
pulsewidth = 0.1; % seconds
pri = 0.5; % seconds
number_of_pulses = 8;

%% Zero Doppler cut

% Set the time delay
time_delay = linspace(-number_of_pulses * pri, number_of_pulses * pri, 5000);

% Calculate the ambiguity function
ambiguity = pulse_train(time_delay, eps, pulsewidth, pri, number_of_pulses);

figure;
plot(time_delay, ambiguity);
xlabel('Time (s)');
ylabel('Relative Amplitude');
title('Pulse Train Ambiguity Function');
grid on;
plot_settings;

%% Zero range cut

% Set the Doppler mismatch
doppler_frequency = linspace(-2.0 / pulsewidth, 2.0 / pulsewidth, 1000);

% Calculate the ambiguity function
ambiguity = pulse_train(eps, doppler_frequency, pulsewidth, pri, number_of_pulses);

figure;
plot(doppler_frequency, ambiguity);
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('Pulse Train Ambiguity Function');
grid on;
plot_settings;

%% 2D contour

% Set the time delay
time_delay = linspace(-number_of_pulses * pri, number_of_pulses * pri, 1000);

% Set the Doppler mismatch
doppler_frequency = linspace(-2.0 / pulsewidth, 2.0 / pulsewidth, 1000);

% Create the grid
[t, f] = meshgrid(time_delay, doppler_frequency);

% Calculate the ambiguity function
ambiguity = pulse_train(t, f, pulsewidth, pri, number_of_pulses);

figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('Pulse Train Ambiguity Function');
grid on;
plot_settings;