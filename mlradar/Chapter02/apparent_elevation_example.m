%% Apparent elevation example
% Created by: Lee A. Harrison
% On: 6/18/2018

clear, clc

% True elevation angle (degrees)
theta_true = 20;

% Target height (km)
height = linspace(0, 5, 100);

% Preallocate the arrays
theta_apparent = zeros(1, numel(height));
theta_apparent_approximate = zeros(1, numel(height));

% Get the apparent elevation angle
for iHeight = 1:numel(height)
    theta_apparent(iHeight) = apparent_elevation(theta_true, height(iHeight));
    theta_apparent_approximate(iHeight) = apparent_elevation_approximate(theta_true, height(iHeight));
end

% Plot the results from the integration
figure;
plot(height, theta_apparent, 'b');
title('Apparent Elevation due to Refraction');
xlabel('Height (km)');
ylabel('Apparent Elevation Angle (degrees)');
grid on; plot_settings;

% Plot the results from the approximate method
figure;
plot(height, theta_apparent_approximate, 'g');
title('Apparent Elevation due to Refraction (Approximate)');
xlabel('Height (km)');
ylabel('Apparent Elevation Angle (degrees)');
grid on; plot_settings;