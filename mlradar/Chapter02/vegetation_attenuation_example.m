%% Vegetation attenuation example
% Created by: Lee A. Harrison
% On: 6/18/2018

% Specific attenuation (dB/m)
specific_attenuation = 0.39;

% Maximum attenuation (dB)
maximum_attenuation = 34.10;

% Distance (m)
distance = linspace(0, 100.0);

% Calculate the attenuation due to vegetation
attenuation = maximum_attenuation * (1. - exp(-distance * specific_attenuation / maximum_attenuation));

% Plot the results
figure;
semilogy(distance, attenuation);
title('Vegetation Attenuation');
xlabel('Distance (m)');
ylabel('Attenuation (dB)');
grid on; plot_settings;