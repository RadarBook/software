%% Single pulse example example
% Created by: Lee A. Harrison
% On: 10/11/2018

clear, clc

% Set the parameters
pfa = 1.0e-6;
pd = 0.99;
number_of_pulses = 10;

np = 1:number_of_pulses;

% Find the required signal to noise for the pd & pfa
required_snr = single_pulse_snr(pd, pfa);

% Calculate the single pulse signal to noise (Curry)
signal_to_noise_reduction = snr_reduction(np, required_snr);

% Calculate the single pulse signal to noise (Peebles)
signal_to_noise_gain = snr_gain(pd, pfa, np, required_snr);

% Calculate the single pulse signal to noise for coherent integration
signal_to_noise_coherent = 10.0 * log10(required_snr ./ np);

% Plot the results
figure;
plot(np, signal_to_noise_coherent); hold on;
plot(np, signal_to_noise_gain);
plot(np, signal_to_noise_reduction);
title('Single Pulse Signal to Noise');
xlabel('Number of Pulses');
ylabel('Signal to Noise (dB)');
grid on;
legend('Coherent Integration', 'Noncoherent Integration (6.22)', 'Noncoherent Integration (6.21)')
plot_settings;