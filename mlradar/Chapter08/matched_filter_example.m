%% Matched filter example
% Created by: Lee A. Harrison
% On: 4/26/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Speed of light
c = 299792458;

% Set the parameters
bandwidth = 20e6; % Hz
pulsewidth = 10e-5; % seconds
target_range = [100, 200, 500]; % meters
target_rcs = [1, 10, 100]; % square meters
window = 'Hanning';

% Number of points in the window
n = (2 * bandwidth * pulsewidth) * 8;

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

% Calculate the baseband return signal
s = zeros(1, n);

% Chirp slope
alpha = 0.5 * bandwidth / pulsewidth;

for i = 1:length(target_range)
    s = s + sqrt(target_rcs(i)) * exp(1j * 2.0 * pi * alpha * (t - 2.0 * target_range(i) / c) .^ 2);
end

% Transmit signal
st = exp(1j * 2 * pi * alpha * t .^ 2);

% Impulse response and matched filtering
Hf = fft(conj(st .* coefficients));
Si = fft(s);
so = fftshift(ifft(Si .* Hf));

% Range window
range_window = linspace(-0.25 * c * pulsewidth, 0.25 * c * pulsewidth, n);

% Plot the results
figure
plot(range_window, 20.0 * log10(abs(so) / n + eps))
xlim([0, max(target_range) + 100]);
ylim([-70, max(20.0 * log10(abs(so) / n)) + 10]);
xlabel('Range (m)')
ylabel('Amplitude (dBsm)')
title('Matched Filter Range Profile')
grid on
plot_settings;