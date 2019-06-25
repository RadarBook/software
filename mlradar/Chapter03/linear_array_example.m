%% Linear array example
% Created by: Lee A. Harrison
% On: 8/3/2018

clear, clc

% Number of elements in the array
number_of_elements = 21;

% Element spacing
element_spacing = 0.5;

% Operating frequency (Hz)
frequency = 300e6;

% Scan angles (rad)
scan_angle = 0.5 * pi;

% Set the theta array
theta = linspace(eps, pi, 1000);

% Sidelobe level for Tschebyscheff coefficients
side_lobe_level = 30.0;

% Window type for the array
window_type = 'Uniform';
% window_type = 'Binomial';
% window_type = 'Tschebyscheff';
% window_type = 'Hanning';
% window_type = 'Hamming';

% New instance of linear_array
la = linear_array(number_of_elements, scan_angle, element_spacing,...
                frequency, theta, window_type, side_lobe_level);

% Get the array factor
af = la.array_factor;

% Plot the array factor
figure;
plot(theta*180/pi, 2*db(abs(af)));
ylim([-60 5]);
title('Linear Array Antenna Pattern');
xlabel('Theta (deg)');
ylabel('Normalized |E| (dB)');
grid on; plot_settings;