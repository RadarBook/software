function [ bp_image ] = backprojection_3d( signal, az, el, ...
    x_image, y_image, z_image, frequency, fft_length)
%% Reconstruct the three-dimensional image using the filtered backprojection method.
%     :param signal: The signal in K-space.
%     :param az: The sensor azimuth positions (rad).
%     :param el: The sensor elevation positions (rad).
%     :param x_image: The image x-coordinates (m).
%     :param y_image: The image y-coordinates (m).
%     :param z_image: The image z-coordinates (m).
%     :param frequency: The frequency array (Hz).
%     :param fft_length: The number of points in the FFT.
%     :return: The reconstructed image.
%
%     Created by: Lee A. Harrison
%     On: 2/9/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Speed of light
c = 299792458;

% Get the frequency step size
frequency_step = frequency(2) - frequency(1);

% Calculate the maximum scene size and resolution
range_extent = c / (2.0 * frequency_step);

% Calculate the range window for the pulses
range_window = linspace(-0.5 * range_extent, 0.5 * range_extent, fft_length);

% Initialize the image
bp_image = zeros(size(x_image));

[nr, nc] = size(az);

% Loop over all pulses in the data
term = 1j * 4.0 * pi * frequency(1) / c;

for row = 1:nr
    
    if mod(50, nr) == 0
        fprintf('Az = %d of %d\n', row, nr);
    end
    
    for col = 1:nc
               
        % Calculate the range profile
        range_profile = fftshift(ifft(signal(:, row, col), fft_length));
        
        % Calculate the range to each pixel
        range_image = x_image * cos(el(row, col)) * cos(az(row, col)) + ...
        y_image * cos(el(row, col)) * sin(az(row, col)) + ...
        z_image * sin(el(row, col));
        
        % Interpolate the range profile onto the image grid and multiply by the range phase
        % For large scenes, should check the range window and index
        bp_image = bp_image + interp1(range_window, range_profile, range_image, 'linear', 0.0) .* exp(term * range_image);
    end
end

end