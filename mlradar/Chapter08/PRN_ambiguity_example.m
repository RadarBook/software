%% PRN ambiguity example
% Created by: Lee A. Harrison
% On: 4/27/2019

clear, clc

% Set the parameters
chip_width = 0.1; % seconds
register_length = 3;

% Force the register length between 2 and 10
if register_length < 2
    register_length = 2;
end

if register_length > 10
    register_length = 10;
end

switch register_length
    case 2
        feedback_taps = [2, 1];
    case 3
        feedback_taps = [3, 2];
    case 4
        feedback_taps = [4, 3];
    case 5
        feedback_taps = [5, 3];
    case 6
        feedback_taps = [6, 5];
    case 7
        feedback_taps = [7, 6];
    case 8
        feedback_taps = [8, 6, 5, 4];
    case 9
        feedback_taps = [9, 5];
    case 10
        feedback_taps = [10, 7];
end

% Generate a maximum length sequence
code = mls(register_length, feedback_taps);

% Calculate the ambiguity function
[ambiguity, time_delay, doppler_frequency] = phase_coded_waveform(code, chip_width);

% Zero Doppler cut
figure;
plot(time_delay, ambiguity(round(length(doppler_frequency) / 2), :));
xlabel('Time (s)');
ylabel('Relative Amplitude');
title('PRN Code Ambiguity Function');
xlim([-length(code) * chip_width, length(code) * chip_width])
grid on;
plot_settings;

% Zero range cut
figure;
plot(doppler_frequency, ambiguity(:, round(length(time_delay) / 2)));
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('PRN Code Ambiguity Function');
grid on;
plot_settings;

% 2D contour
[t, f] = meshgrid(time_delay, doppler_frequency);
figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('PRN Code Ambiguity Function');
xlim([-length(code) * chip_width, length(code) * chip_width])
grid on;
plot_settings;