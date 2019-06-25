%% Loop example
% Created by: Lee A. Harrison
% On: 8/5/2018

clear, clc

% The operating frequency (Hz)
frequency = 1.0e9;

% The current on the loop (A)
current = 1.0;

% The radius of the loop (m)
radius = 0.1;

% Angluar span for the pattern (rad)
theta = linspace(0.0, 2.0 * pi, 1000);

% A new instance of loop antenna
%loop = small_loop(radius, current, frequency, 1e6, theta);
loop = circular_loop(radius, current, frequency, 1e6, theta);

% Calculate the directivity
d = loop.directivity;
fprintf('Directivity = %.2f\n', d);

% Calculate the beamwidth
b = loop.beamwidth;
fprintf('Beamwidth = %.2f (deg)\n', b);

% Calculate the maximum effective aperture
ae = loop.maximum_effective_aperture;
fprintf('Maximum Effective Aperture = %.2e (m^2)\n', ae);

% Calculate the radiation resistance
rr = loop.radiation_resistance;
fprintf('Radiation Resistance = %.2f (Ohms)\n', rr);

% Calculate the radiated power
prad = loop.radiated_power;
fprintf('Total Power Radiated = %.2f (W)\n', prad);

% Calculate the far fields
[e_r, e_theta, e_phi, h_r, h_theta, h_phi] = loop.far_field;

% Calculate the normalized magnitude of the electric field
e_mag = sqrt(abs(e_phi .* e_phi));
e_mag = e_mag ./ max(max(e_mag));

% Plot the results
figure;
polar(theta, (e_mag));
% polarplot(theta, (e_mag));
title('Loop Antenna Pattern');
grid on; plot_settings;