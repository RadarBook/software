%% ADC example
% Created by: Lee A. Harrison
% On: 9/19/2018

clear, clc

% Set the parameters
number_of_bits = 3;
sampling_frequency = 100;
start_frequency = 1.0;
end_frequency = 4.0;
am_amplitude = 0.1;
am_frequency = 4.0;

% Analog signal for plotting
t = linspace(0.0, 1.0, 4196);
a_signal = chirp(t, start_frequency, t(end), end_frequency);
a_signal = a_signal .* (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * t));

% Set up the waveform
time = (0:sampling_frequency) / sampling_frequency;
if_signal = chirp(time, start_frequency, time(end), end_frequency);
if_signal = if_signal .* (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * time));

% Calculate the envelope
[quantized_signal, error_signal] = quantization(if_signal, number_of_bits);

% Plot the results
figure;
subplot(2,1,1)
plot(t, a_signal); hold on;
plot(time, quantized_signal, 'r--');
ylabel('Amplitude (V)');
title('Analog to Digital Conversion');
grid on;
legend('Analog Signal', 'Digital Signal')

subplot(2,1,2)
plot(time, error_signal);
xlabel('Time (s)');
ylabel('Error (V)');
grid on;

plot_settings;