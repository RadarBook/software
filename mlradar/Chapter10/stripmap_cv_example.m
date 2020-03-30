%% Stripmap CV example
% Created by: Lee A. Harrison
% On: 3/28/2020

clear, clc

% Speed of light
c = 299792458;

% Set the squint angle (rad)
squint_angle = 0 * pi / 180;

% Set the x and y center of the image (m)
x_center = 1e3;
y_center = x_center * tan(squint_angle);

% Set the x and y span of the image (m)
x_span = 10;
y_span = 10;

% Set the number of bins in the x and y direction
nx = 200;
ny = 200;

% Set the aperture length and antenna width (m)
aperture_length = 100;
antenna_width = 2;

% Set the window type and dynamic range (dB)
window_type = 'None';
dynamic_range = 50;

% Load the selected target
load('Jeep99_el30.0000.mat');

% Set the polarization
signal = data.vv;

% Set up the image space
xi = linspace(-0.5 * x_span + x_center, 0.5 * x_span + x_center, nx);
yi = linspace(-0.5 * y_span + y_center, 0.5 * y_span + y_center, ny);
[x_image, y_image] = meshgrid(xi, yi);
z_image = zeros(size(x_image));

% Get the sensor frequency (Hz)
frequency = data.FGHz * 1e9;

% Set the fft length
fft_length = 4 * 2^nextpow2(length(frequency));

% Calculate the wavelength at the start frequency (m)
wavelength = c / frequency(1);

% Calculate the number of frequencies and the bandwidth (Hz)
bandwidth = frequency(end) - frequency(1);
number_of_frequencies = length(frequency);

% Calculate the element spacing (m)
element_spacing = wavelength / 4.0;

% Calculate the number of elements
number_of_elements = ceil(antenna_width / element_spacing + 1);

% Calculate the spacing on the synthetic aperture (m)
aperture_spacing = tan(c / (2 * y_span * frequency(1))) * x_center;  % Based on y_span

% Calculate the number of samples (pulses) on the aperture
number_of_samples = ceil(aperture_length / aperture_spacing + 1);

% Create the aperture
synthetic_aperture = linspace(-0.5 * aperture_length, 0.5 * aperture_length, number_of_samples);

% Calculate the sensor location
sensor_x = zeros(size(synthetic_aperture));
sensor_y = synthetic_aperture;
sensor_z = zeros(size(synthetic_aperture));

% Initialize the signal
signal1 = zeros(number_of_frequencies, number_of_samples);

% Initialize the range center (m)
range_center = zeros(size(synthetic_aperture));

% For calculating sensor height
te = tan(deg2rad(data.elev));

% Calculate the signal (k space)
for i_ap = 1:length(synthetic_aperture)
    
    % Calculate the sensor z location
    sensor_z(i_ap) = sqrt(x_center ^ 2 + (y_center - synthetic_aperture(i_ap)) ^ 2) * te;

    % Calculate the range to the center of the scene (m)
    range_center(i_ap) = sqrt(x_center ^ 2 + (y_center - synthetic_aperture(i_ap)) ^ 2 + sensor_z(i_ap) ^ 2);

    % Calculate the target azimuth (rad)
    target_azimuth = atan((y_center - synthetic_aperture(i_ap)) / x_center);
    target_azimuth = mod(target_azimuth, 2 * pi);

    % Find the value of the antenna pattern at the target azimuth
    la = linear_array(number_of_elements, 0.5 * pi - squint_angle, element_spacing, frequency(1), target_azimuth, 'Uniform', -100);
    antenna_pattern = la.array_factor_un * cos(squint_angle);
    
    % Calculate the return signal
    [~, i_close] = min(abs(rad2deg(target_azimuth) - data.azim));
    signal1(:, i_ap) = antenna_pattern ^ 2 * signal(:, i_close);
   
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
signal1 = signal1 .* coefficients;

% Reconstruct the image
bp_image = backprojection(signal1, sensor_x, sensor_y, sensor_z, range_center, x_image, y_image, z_image, frequency, fft_length);

% Display the results
bpi = abs(bp_image) ./ max(max(abs(bp_image)));
pcolor(xi, yi, 20.0 * log10(bpi)); shading flat;
caxis([-dynamic_range, 0.0])
h = colorbar;
ylabel(h, 'dB');

% Set the plot title and labels
title(sprintf('Stripmap SAR - Squint %d^o', squint_angle * 180 / pi))
xlabel('Range (m)')
ylabel('Cross Range (m)')
axis('square')
plot_settings;