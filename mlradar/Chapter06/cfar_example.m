%% CFAR example
% Created by: Lee A. Harrison
% On: 10/11/2018

clear, clc

% Set the parameters
cfar_type = 'Cell Averaging';
%cfar_type = 'Cell Averaging Greatest Of';
%cfar_type = 'Cell Averaging Smallest Of';
%cfar_type = 'Ordered Statistic';

guard_cells = 2;
reference_cells = 10;
bias = 3.0;

% Generate a sample signal to be used (later used matched filter output)
number_of_samples = 1000;
i_noise = 0.05 * randn(1, number_of_samples); 
q_noise = 0.05 * randn(1, number_of_samples); 

noise_signal = sqrt(i_noise .^ 2 + q_noise .^ 2);

t = linspace(0.0, 1.0, number_of_samples);

s1 = 0.4 * cos(2 * pi * 600 * t) + 1j * 0.4 * sin(2 * pi * 600 * t);
s2 = 0.1 * cos(2 * pi * 150 * t) + 1j * 0.1 * sin(2 * pi * 150 * t);
s3 = 0.2 * cos(2 * pi * 100 * t) + 1j * 0.2 * sin(2 * pi * 100 * t);

% Sum for the example signal
signal = abs(fft(s1 + s2 + s3 + noise_signal));
signal(1) = 0;

% Calculate the CFAR threshold
cfar_threshold = cfar(signal, guard_cells, reference_cells, bias, cfar_type);

% Plot the results
figure;
plot(t, 10 * log10(signal)); hold on;
plot(t, cfar_threshold);
title('Constant False Alarm Rate');
xlabel('Range (m)');
ylabel('Signal Strength (dB)');
legend('Signal', 'CFAR Threshold');
grid on;
plot_settings;