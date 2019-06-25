%% Backprojection 3D example
% Created by: Lee A. Harrison
% On: 5/1/2019

clear, clc

% Speed of light
c = 299792458;

% Set the locations of the scatterers (m)
x_target = [3, -3, 3, -3];
y_target = [3, -3, -3, 3];
z_target = [-3, -3, 3, 3];

% Set the RCS of the scatterers (m^2)
rcs = [10, 10, 20, 20];

% Set the image span (m)
x_span = 10;
y_span = 10;
z_span = 10;

% Number of bins in x, y and z
nx = 20;
ny = 20;
nz = 20;

% Specify the starting frequency and bandwidth (Hz)
start_frequency = 5e9;
bandwidth = 1e9;

% Set the angular span (deg)
az_start = 0;
az_end = 1;

el_start = 0;
el_end = 1;

% Set the dynamic range (dB)
dynamic_range = 30;

% Set the window type
window_type = 'None';

% Set up the azimuth space
r = sqrt(x_span ^ 2 + y_span ^ 2);
da = c / (2.0 * r * start_frequency);
na = round((az_end - az_start) / da);
az = linspace(az_start, az_end, na);

% Set up the elevation space
r = sqrt(x_span ^ 2 + z_span ^ 2);
de = c / (2.0 * r * start_frequency);
ne = round((el_end - el_start) / de);
el = linspace(el_start, el_end, ne);

% Set up the angular grid
[az_grid, el_grid] = meshgrid(az, el);

% Set up the frequency space
df = c / (2.0 * r);
nf = round(bandwidth / df);
frequency = linspace(start_frequency, start_frequency + bandwidth, nf);

% Set the length of the FFT
fft_length = 8 * 2^nextpow2(nf);

% Set up the image space
xi = linspace(-0.5 * x_span, 0.5 * x_span, nx);
yi = linspace(-0.5 * y_span, 0.5 * y_span, ny);
zi = linspace(-0.5 * z_span, 0.5 * z_span, nz);
[x_image, y_image, z_image] = meshgrid(xi, yi, zi);

signal = zeros(nf, ne, na);

% Calculate the signal (k space)
az = deg2rad(az);
el = deg2rad(el);
for i1 = 1:length(az)
    for i2 = 1:length(el)
        r_los = [cos(el(i2)) * cos(az(i1)), cos(el(i2)) * sin(az(i1)), sin(el(i2))];
        for i = 1:length(x_target)
            r_target = dot(r_los, [x_target(i), y_target(i), z_target(i)]);
            signal(:, i2, i1) = signal(:, i2, i1) + r * exp(-1j * 4.0 * pi * frequency / c * r_target)';
        end
    end
end

% Get the window coefficients
coefficients = ones(nf, ne, na);

switch window_type
    case 'Hanning'
        h1 = hanning(nf);
        h2 = hanning(na);
        h3 = hanning(ne);
        for i = 1:nf
            for j = 1:ne
                for k = 1:na
                    coefficients(i, j, k) = (h1(i) * h2(k) * h3(j)) ^ (1/3);
                end
            end
        end
    case 'Hamming'
        h1 = hamming(nf);
        h2 = hamming(na);
        h3 = hamming(ne);
        for i = 1:nf
            for j = 1:ne
                for k = 1:na
                    coefficients(i, j, k) = (h1(i) * h2(k) * h3(j)) ^ (1/3);
                end
            end
        end
end

% Apply the selected window
signal = signal .* coefficients;

% Reconstruct the image
bp_image = backprojection_3d(signal, deg2rad(az_grid), deg2rad(el_grid),...
    x_image, y_image, z_image, frequency, fft_length);

a = abs(bp_image) ./ max(max(max(abs(bp_image))));

i = a > 10.0 ^ (-dynamic_range/20.0);

xs = x_image(i);
ys = y_image(i);
zs = z_image(i);
rs = a(i) * 10.0;

% Display the results
scatter3(xs, ys, zs, rs, 'filled')

% Set the plot title and labels
title('Back Projection')
xlabel('X (m)')
ylabel('Y (m)')
zlabel('Z (m)')

axis('square');
plot_settings;