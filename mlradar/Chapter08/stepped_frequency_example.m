%% Stepped frequency example
% Created by: Lee A. Harrison
% On: 4/27/2019

clear, clc

% Speed of light
c = 299792458;

% Set the parameters
number_of_steps = 64;
frequency_step = 50e3;
prf = 100;
target_range = [0.5e3, 1.5e3, 2.0e3];
target_rcs = [1, 10, 100];
target_velocity = [0, 0, 10];
window = 'None';

switch window
    case 'Hanning'
        coefficients = hanning(number_of_steps);
    case 'Hamming'
        coefficients = hamming(number_of_steps);
    case 'Kaiser'
        coefficients = kaiser(number_of_steps, 6);
    case 'None'
        coefficients = ones(1, number_of_steps);
end

% Calculate the base band return signal
s = 0;

for m = 1:length(target_range)
    s0 = zeros(number_of_steps, 1);
    for i = 1:number_of_steps
        s0(i) = sqrt(target_rcs(m)) * exp(-1j * 4.0 * pi / c * (i * frequency_step) ...
            * (target_range(m) - target_velocity(m) * (i / prf)));
    end
    s = s + s0;
end

n = 2^nextpow2(10 * number_of_steps);
sf = ifft(s .* coefficients', n) * n / number_of_steps;

% range_resolution = c / (2.0 * number_of_steps * frequency_step)
range_unambiguous = c / (2.0 * frequency_step);

range_window = linspace(0, range_unambiguous, n);

% Plot the results
figure
plot(range_window, 20.0 * log10(abs(sf) / n + eps))
xlabel('Range (m)')
ylabel('Amplitude (dBsm)')
title('Stepped Frequency Range Profile')
grid on
plot_settings;