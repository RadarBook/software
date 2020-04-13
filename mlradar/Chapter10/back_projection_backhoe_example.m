%% Backprojection backhoe example
% Created by: Lee A. Harrison
% On: 5/1/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Speed of light
c = 299792458;

% Set the image span (m)
x_span = 10;
y_span = 10;
z_span = 10;

% Number of bins in x, y and z
nx = 10;
ny = 10;
nz = 10;

% Set the angular span (deg)
az_start = 66;
az_end = 71;

el_start = 18;
el_end = 23;

% Set the dynamic range (dB)
dynamic_range = 50;

% Set the polarization
polarization = 'HH';

% Set the window type
window_type = 'None';

x = linspace(-0.5 * x_span, 0.5 * x_span, nx);
y = linspace(-0.5 * y_span, 0.5 * y_span, ny);
z = linspace(-0.5 * z_span, 0.5 * z_span, nz);
[x_image, y_image, z_image] = meshgrid(x, y, z);

% Set the FFT length for this dataset
fft_length = 8192;

% Initialize the image
bp_image = 0;

% Loop over the azimuth and elevation angles
for ie = el_start:el_end
    for ia = az_start:az_end
        fprintf('El %d  Az %d\n', ie, ia);
        
        % Load the files
        filename = sprintf('backhoe_el%03d_az%03d.mat', ie, ia);
        load(filename);
        
        % Select the polarization
        switch polarization
            case 'VV'
                signal = data.vv;
            case 'HH'
                signal = data.hh;
            case 'HV'
                signal = data.vhhv;
        end
        sensor_az = deg2rad(data.azim);
        sensor_el = deg2rad(data.elev);
        frequency = data.FGHz * 1e9;
        
        nf = length(frequency);
        na = length(sensor_az);
        ne = length(sensor_el);
        
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
        bp_image = bp_image + backprojection_3d(signal, sensor_az, sensor_el, x_image, ...
            y_image, z_image, frequency, fft_length);
    end
end

% Normalize the image
a = abs(bp_image) ./ max(max(max(abs(bp_image))));

% Find the data above the dynamic range
i = a > 10.0 ^ (-dynamic_range/20.0);

% Set the points for the scatter plot
xs = x_image(i);
ys = y_image(i);
zs = z_image(i);
rs = a(i) * 10.0;

% Display the results
figure; scatter3(xs, ys, zs, rs, 'filled')

% Set the plot title and labels
title('Back Projection')
xlabel('X (m)')
ylabel('Y (m)')
zlabel('Z (m)')
axis('square');
plot_settings;