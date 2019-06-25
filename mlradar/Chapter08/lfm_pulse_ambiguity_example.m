%% LFM pulse ambiguity example
% Created by: Lee A. Harrison
% On: 4/26/2019

clear, clc

% Set the parameters
bandwidth = 2e3; % Hz
pulsewidth = 1e-3; % seconds

%% Zero Doppler cut

% Set the time delay
time_delay = linspace(-pulsewidth, pulsewidth, 5000);

% Calculate the ambiguity function
ambiguity = lfm_pulse(time_delay, eps, pulsewidth, bandwidth);

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
ambiguity = lfm_pulse(eps, doppler_frequency, pulsewidth, bandwidth);

figure;
plot(doppler_frequency, ambiguity);
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('LFM Pulse Ambiguity Function');
grid on;
plot_settings;

%% 2D contour

% Set the time delay
time_delay = linspace(-pulsewidth, pulsewidth, 500);

% Set the Doppler mismatch
doppler_frequency = linspace(-bandwidth, bandwidth, 500);

% Create the grid
[t, f] = meshgrid(time_delay, doppler_frequency);

% Calculate the ambiguity function
ambiguity = lfm_pulse(t, f, pulsewidth, bandwidth);

figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('LFM Pulse Ambiguity Function');
grid on;
plot_settings;