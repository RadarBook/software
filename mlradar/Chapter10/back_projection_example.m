%% Backprojection example
% Created by: Lee A. Harrison
% On: 4/30/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Speed of light
c = 299792458;

% Set the parameters
range_center = 1000; % meters
x_target = [3, 0, -3]; % meters
y_target = [-3, 0, 3]; % meters
rcs = [10, 10, 20]; % m^2
x_span = 20; % meters
y_span = 20; % meters
nx = 200; % Number of bins in x-direction
ny = 200; % Number of bins in y-direction
start_frequency = 5e9; % Staring frequency (Hz)
bandwidth = 300e6; % Operating bandwidth (Hz)
az_start = -3; % degrees
az_end = 3; % degrees
window_type = 'None';
dynamic_range = 50; % dB

% Set up the azimuth space
r = sqrt(x_span ^ 2 + y_span ^ 2);
da = c / (2.0 * r * start_frequency);
na = round((az_end - az_start) / da);
az = linspace(az_start, az_end, na);

% Set up the frequency space
df = c / (2.0 * r);
nf = floor(bandwidth / df);
frequency = linspace(start_frequency, start_frequency + bandwidth, nf);

% Set the length of the FFT
fft_length = 8 * 2^nextpow2(nf);

% Set up the aperture positions
sensor_x = range_center * cos(deg2rad(az));
sensor_y = range_center * sin(deg2rad(az));
sensor_z = zeros(size(sensor_x));

% Set up the image space
xi = linspace(-0.5 * x_span, 0.5 * x_span, nx);
yi = linspace(-0.5 * y_span, 0.5 * y_span, ny);
[x_image, y_image] = meshgrid(xi, yi);
z_image = zeros(size(x_image));

% Calculate the signal (k space)
signal = zeros(nf, na);

index = 0;

for i = 1:na
    r_los = [cos(deg2rad(az(i))), sin(deg2rad(az(i)))];
    for j = 1:length(x_target)
        r_target = dot(r_los, [x_target(j), y_target(j)]);
        signal(:, i) = signal(:, i) + rcs(j) * exp(-1j * 4.0 * pi * frequency / c * r_target)';
    end
end

% Get the window
switch window_type
    case 'Hanning'
        h1 = hanning(nf);
        h2 = hanning(na);
        coefficients = sqrt(h1' * h2);
    case 'Hamming'
        h1 = hamming(nf);
        h2 = hamming(na);
        coefficients = sqrt(h1' * h2);
    case 'None'
        coefficients = ones(nf, na);
end

% Apply the selected window
signal = signal .* coefficients;

% Reconstruct the image
bp_image = backprojection(signal, sensor_x, sensor_y, sensor_z, range_center, ...
    x_image, y_image, z_image, frequency, fft_length);

% Display the results
bpi = abs(bp_image) ./ max(max(abs(bp_image)));
pcolor(xi, yi, 20.0 * log10(bpi)); shading flat;
caxis([-dynamic_range, 0.0])
h = colorbar;
ylabel(h, 'dB');

% Set the plot title and labels
title('Back Projection')
xlabel('Range (m)')
ylabel('Cross Range (m)')
axis('square')
plot_settings;