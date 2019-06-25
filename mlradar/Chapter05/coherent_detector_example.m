%% Coherent detector example
% Created by: Lee A. Harrison
% On: 9/19/2018

clear, clc

% Set the parameters
sampling_frequency = 400;
start_frequency = 20;
end_frequency = 80;
am_amplitude = 0.1;
am_frequency = 4;

% Calculate the bandwidth and center frequency
bandwidth = end_frequency - start_frequency;
center_frequency = 0.5 * bandwidth + start_frequency;

% Set up the waveform
time = (0:sampling_frequency-1) / sampling_frequency;
if_signal = chirp(time, start_frequency, time(end), end_frequency);
if_signal = if_signal .* (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * time));


% Calculate the baseband I and Q
[i_signal, q_signal] = coherent_detector(if_signal, center_frequency, bandwidth, sampling_frequency, time);

% Plot the results
figure;
plot(time, i_signal); hold on;
plot(time, q_signal, 'r--');
title('Coherent Detector');
xlabel('Time (s)');
ylabel('Amplitude (V)');
grid on;
legend('In Phase', 'Quadrature');

plot_settings;