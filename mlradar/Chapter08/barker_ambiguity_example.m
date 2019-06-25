%% Barker ambiguity example
% Created by: Lee A. Harrison
% On: 4/26/2019

clear, clc

% Set the parameters
chip_width = 0.1; % seconds
code_length = 4; % 2, 3, 4, 5, 7, 11, 13

% Select the Barker code
switch code_length
    case 2
        code = [1, -1];
    case 3
        code = [1, 1, -1];
    case 4
        code = [1, 1, -1, 1];
    case 5
        code = [1, 1, 1, -1, 1];
    case 7
        code = [1, 1, 1, -1, -1, 1, -1];
    case 11
        code = [1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1];
    case 13
        code = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1];
end

% Calculate the ambiguity function
[ambiguity, time_delay, doppler_frequency] = phase_coded_waveform(code, chip_width);

% Zero Doppler cut
figure;
plot(time_delay, ambiguity(round(length(doppler_frequency) / 2), :));
xlabel('Time (s)');
ylabel('Relative Amplitude');
title('Barker Code Ambiguity Function');
xlim([-length(code) * chip_width, length(code) * chip_width])
grid on;
plot_settings;

% Zero range cut
figure;
plot(doppler_frequency, ambiguity(:, round(length(time_delay) / 2)));
xlabel('Doppler (Hz)');
ylabel('Relative Amplitude');
title('Barker Code Ambiguity Function');
grid on;
plot_settings;

% 2D contour
[t, f] = meshgrid(time_delay, doppler_frequency);
figure;
contour(t, f, ambiguity, 30);
xlabel('Time (s)');
ylabel('Doppler (Hz)');
title('Barker Code Ambiguity Function');
xlim([-length(code) * chip_width, length(code) * chip_width])
grid on;
plot_settings;