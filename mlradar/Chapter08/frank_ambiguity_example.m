%% Frank ambiguity example
% Created by: Lee A. Harrison
% On: 4/26/2019

clear, clc

% Set the parameters
n_phase = 3; % N-phase Frank code
chip_width = 0.1; % seconds

% Get the N-phase Frank code
code = n_phase_code(n_phase);

% Calculate the ambiguity function
[ambiguity, time_delay, doppler_frequency] = phase_coded_waveform(code, chip_width);

% Zero Doppler cut
figure;
plot(time_delay, ambiguity(round(length(doppler_frequency) / 2), :));
xlabel('Time (s)');
ylabel('Relative Amplitude');
title('Frank Code Ambiguity Function');
xlim([-length(code) * chip_width, length(code) * chip_width])
grid on;
plot_settings;

% Zero range cut
figure;
plot(doppler_frequency, ambiguity(:, round(length(time_delay) / 2)));
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('Frank Code Ambiguity Function');
grid on;
plot_settings;

% 2D contour
[t, f] = meshgrid(time_delay, doppler_frequency);
figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('Frank Code Ambiguity Function');
xlim([-length(code) * chip_width, length(code) * chip_width])
grid on;
plot_settings;