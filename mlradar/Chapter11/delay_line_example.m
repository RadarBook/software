%% Delay line example
% Created by: Lee A. Harrison
% On: 5/28/2019

clear, clc

% Set the parameters
type = 'Single';
type = 'Stagger';

% PRF stagger
prf_stagger = 1.25;

% Normalized frequency
frequency = linspace(0, 4, 1000);

% Calculate the response based on the type
if strcmp(type, 'Single')
    gain = sin(pi * frequency) .^ 2;
    
    % Display the results
    plot(frequency, db(gain + eps));
else
    gain_prf1 = sin(pi * frequency) .^ 2;
    gain_prf2 = sin(pi * frequency * prf_stagger) .^ 2;
    gain_total = 0.5 * (gain_prf1 + gain_prf2);
    
    % Display the results
    plot(frequency, db(gain_prf1 + eps)); hold on;
    plot(frequency, db(gain_prf2 + eps), 'r--');
    plot(frequency, db(gain_total + eps), 'g-.');
    legend('PRF1', 'PRF2', 'PRF Staggered');
end

% Title and labels
title('Delay Line Response');
xlabel('Normalized Frequency (f / PRF)');
ylabel('Power Gain (dB)');

% Set the y-axis limits
ylim([-30 0.0]);

% Turn on the grid
grid on;

% Plot settings
plot_settings;