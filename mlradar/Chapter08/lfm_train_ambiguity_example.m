%% LFM train ambiguity example
% Created by: Lee A. Harrison
% On: 4/26/2019

clear, clc

% Set the parameters
bandwidth = 10; % Hz
pulsewidth = 0.4; % seconds
pri = 1; % seconds
number_of_pulses = 6;

%% Zero Doppler cut

% Set the time delay
time_delay = linspace(-number_of_pulses * pri, number_of_pulses * pri, 5000);

% Calculate the ambiguity function
ambiguity = lfm_train(time_delay, eps, pulsewidth, bandwidth, pri, number_of_pulses);

figure;
plot(time_delay, ambiguity);
xlabel('Time (s)');
ylabel('Relative Amplitude');
title('LFM Pulse Ambiguity Function');
grid on;
plot_settings;

%% Zero range cut

% Set the Doppler mismatch
doppler_frequency = linspace(-bandwidth, bandwidth, 5000);

% Calculate the ambiguity function
ambiguity = lfm_train(eps, doppler_frequency, pulsewidth, bandwidth, pri, number_of_pulses);

figure;
plot(doppler_frequency, ambiguity);
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('LFM Pulse Ambiguity Function');
grid on;
plot_settings;

%% 2D contour

% Set the time delay
time_delay = linspace(-number_of_pulses * pri, number_of_pulses * pri, 1000);

% Set the Doppler mismatch
doppler_frequency = linspace(-bandwidth, bandwidth, 1000);

% Create the grid
[t, f] = meshgrid(time_delay, doppler_frequency);

% Calculate the ambiguity function
ambiguity = lfm_train(t, f, pulsewidth, bandwidth, pri, number_of_pulses);

figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('LFM Pulse Ambiguity Function');
grid on;
plot_settings;