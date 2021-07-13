%% Stripmap example
% Created by: Lee A. Harrison
% On: 3/28/2020
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Speed of light
c = 299792458;

% Set the squint angle (rad)
squint_angle = 10 * pi / 180;

% Set the x and y center of the image (m)
x_center = 1e3;
y_center = x_center * tan(squint_angle);

% Set the target locations (m) and reflectivity
xt = [-3, 2];
yt = [4, -1];
rt = [1, 10];

% Set the x and y span of the image (m)
x_span = 12;
y_span = 12;

% Set the number of bins in the x and y direction
nx = 200;
ny = 200;

% Set the start frequency and bandwith (Hz)
start_frequency = 1e9;
bandwidth = 300e6;

% Set the aperture length and antenna width (m)
aperture_length = 200;
antenna_width = 2;

% Set the window type (Rectangular, Hanning, or Hamming)
window_type = 'None';

% Set the dynamic range of the image (dB)
dynamic_range = 40;

% Set up the image space
xi = linspace(-0.5 * x_span + x_center, 0.5 * x_span + x_center, nx);
yi = linspace(-0.5 * y_span + y_center, 0.5 * y_span + y_center, ny);

[x_image, y_image] = meshgrid(xi, yi);
z_image = zeros(size(x_image));

% Calculate the wavelength at the start frequency (m)
wavelength = c / start_frequency;

% Calculate the number of frequencies
df = c / (2.0 * sqrt(x_span ^ 2 + y_span ^ 2));
number_of_frequencies = ceil(bandwidth / df);

% Set up the frequency space
frequency = linspace(start_frequency, start_frequency + bandwidth, number_of_frequencies);

% Set the length of the FFT
fft_length = 2 ^ nextpow2(4 * number_of_frequencies);

% Calculate the element spacing (m)
element_spacing = wavelength / 4.0;

% Calculate the number of elements
number_of_elements = ceil(antenna_width / element_spacing + 1);

% Calculate the spacing on the synthetic aperture (m)
aperture_spacing = tan(c / (2 * y_span * start_frequency)) * x_center; % Based on y_span

% Calculate the number of samples (pulses) on the aperture
number_of_samples = ceil(aperture_length / aperture_spacing + 1);

% Create the aperture
synthetic_aperture = linspace(-0.5 * aperture_length, 0.5 * aperture_length, number_of_samples);

% Calculate the sensor location
sensor_x = zeros(size(synthetic_aperture));
sensor_y = synthetic_aperture;
sensor_z = zeros(size(synthetic_aperture));

% Initialize the signal
signal = zeros(number_of_frequencies, number_of_samples);

% Initialize the range center (m)
range_center = zeros(size(synthetic_aperture));

% Phase term for the range phase (rad)
phase_term = -1j * 4.0 * pi * frequency / c;

% Calculate the signal (k space)
for i_ap = 1:length(synthetic_aperture)
    range_center(i_ap) = sqrt(x_center ^ 2 + (y_center - synthetic_aperture(i_ap)) ^ 2);
    
    for i_targ = 1:length(xt)
        %Antenna pattern at each target
        target_range = sqrt((x_center + xt(i_targ)) ^ 2 + (y_center + yt(i_targ) - synthetic_aperture(i_ap)) ^ 2) - range_center(i_ap);
        target_azimuth = atan((y_center + yt(i_targ) - synthetic_aperture(i_ap)) / (x_center + xt(i_targ)));
        % Calculate the array factor
        la = linear_array(number_of_elements, 0.5 * pi - squint_angle, element_spacing, frequency(1), 0.5 * pi - target_azimuth, 'Uniform', -100);
        antenna_pattern = la.array_factor_un * cos(squint_angle);
        signal(:, i_ap) = signal(:, i_ap) + rt(i_targ) * antenna_pattern ^ 2 * exp(phase_term * target_range)';
    end
end

% Get the window
switch window_type
    case 'Hanning'
        h1 = hanning(number_of_frequencies);
        h2 = hanning(number_of_samples);
        coefficients = sqrt(h1' * h2);
    case 'Hamming'
        h1 = hamming(number_of_frequencies);
        h2 = hamming(number_of_samples);
        coefficients = sqrt(h1' * h2);
    case 'None'
        coefficients = ones(number_of_frequencies, number_of_samples);
end

% Apply the selected window
signal = signal .* coefficients;

% Reconstruct the image
bp_image = backprojection(signal, sensor_x, sensor_y, sensor_z, range_center, x_image, y_image, z_image, frequency, fft_length);

% Display the results
bpi = abs(bp_image) ./ max(max(abs(bp_image)));
pcolor(xi, yi, 20.0 * log10(bpi)); shading flat;
caxis([-dynamic_range, 0.0])
h = colorbar;
ylabel(h, 'dB');

% Set the plot title and labels
title(sprintf('Stripmap SAR - Squint Angle %d^o', squint_angle * 180 / pi))
xlabel('Range (m)')
ylabel('Cross Range (m)')
axis('square')
plot_settings;