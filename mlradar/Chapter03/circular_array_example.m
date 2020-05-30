%% Circular array example
% Created by: Lee A. Harrison
% On: 8/3/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Number of elements in the array
number_of_elements = 21;

% Radius of the array (m)
radius = 0.5; 

% Operating frequency (Hz)
frequency = 300.0e6;

% Scan angles (rad)
scan_angle_theta = 0.0;
scan_angle_phi = 0.0;

% Set the theta and phi grid
n = 360;
m = floor(n/4);
[theta, phi] = meshgrid(linspace(0.0, 0.5 * pi, n), linspace(0.0, 2.0 * pi, n));

% New instance of circular_array
ca = circular_array(number_of_elements, radius, frequency, scan_angle_theta, scan_angle_phi, theta, phi);

% Get the array factor
af = ca.array_factor;

% U-V coordinates for plotting the antenna pattern
uu = sin(theta) .* cos(phi);
vv = sin(theta) .* sin(phi);

% Plot the array factor
figure;
pcolor(uu, vv, abs(af)); shading flat
xlabel('U (sines)');
ylabel('V (sines)');
title('Circular Array Antenna Pattern');
axis equal
plot_settings;


figure;
plot(theta(1,:)*180/pi, 2*db(abs(af(m,:)))); hold on;
plot(theta(1,:)*180/pi, 2*db(abs(af(1,:)))); 
ylim([-60 5]);
title('Circular Array Antenna Pattern');
xlabel('Theta (deg)');
ylabel('Normalized |E| (dB)');
legend('E-plane', 'H-plane');
grid on; plot_settings;