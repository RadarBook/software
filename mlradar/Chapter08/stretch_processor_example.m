%% Stretch processor example
% Created by: Lee A. Harrison
% On: 4/27/2019

clear, clc

% Speed of light
c = 299792458;

% Set the parameters
bandwidth = 1e9; % Hz
pulsewidth = 10e-4; % seconds
range_window_length = 50.0; % meters
target_range = [5, 15]; % meters
target_rcs = [20, 10]; % square meters
window = 'None';

% Number of samples
n = ceil(4 * bandwidth * range_window_length / c);

switch window
    case 'Hanning'
        coefficients = hanning(n);
    case 'Hamming'
        coefficients = hamming(n);
    case 'Kaiser'
        coefficients = kaiser(n, 6);
    case 'None'
        coefficients = ones(1, n);
end

% Set up the time vector
t = linspace(-0.5 * pulsewidth, 0.5 * pulsewidth, n);

% Sampled signal after mixing
so = 0;

for i = 1:length(target_range)
    so = so + sqrt(target_rcs(i)) * exp(1j * 2.0 * pi * bandwidth / pulsewidth * (2 * target_range(i) / c) * t);
end

% Fourier transform
so = fftshift(fft(so .* coefficients, 4 * n));

% FFT frequencies
frequencies = fftshift(fftfreq(4 * n, t(2) - t(1)));

% Range window
range_window = 0.5 * frequencies * c * pulsewidth / bandwidth;

% Plot the results
figure
plot(range_window, 20.0 * log10(abs(so) / n + eps))
xlim([min(target_range) - 5, max(target_range) + 5]);
ylim([-60, max(20.0 * log10(abs(so) / n)) + 10]);
xlabel('Range (m)')
ylabel('Amplitude (dBsm)')
title('Stretch Processor Range Profile')
grid on
plot_settings;