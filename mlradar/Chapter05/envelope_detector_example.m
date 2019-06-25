%% Envelope detector example
% Created by: Lee A. Harrison
% On: 9/19/2018

clear, clc

% Set the parameters

sampling_frequency = 400;
start_frequency = 20;
end_frequency = 80;
am_amplitude = 0.1;
am_frequency = 4;

% Set up the waveform
time = (0:sampling_frequency - 1) / sampling_frequency;
if_signal = chirp(time, start_frequency, time(end), end_frequency);
if_signal = if_signal .* (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * time));

% Calculate the envelope
envelope = envelope_detector(if_signal);

% Plot the results
figure;
plot(time, if_signal); hold on;
plot(time, envelope, 'r--');

title('Envelope Detector');
xlabel('Time (s)');
ylabel('Amplitude (V)');

grid on;

legend('IF Signal', 'Envelope')

plot_settings;