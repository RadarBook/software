function [ bp_image ] = backprojection( signal, sensor_x, sensor_y, sensor_z, range_center, x_image, y_image, z_image, frequency, fft_length )
%% Reconstruct the two-dimensional image using the filtered backprojection method.
%     :param signal: The signal in K-space.
%     :param sensor_x: The sensor x-coordinate (m).
%     :param sensor_y: The sensor y-coordinate (m).
%     :param sensor_z: The sensor z-coordinate (m).
%     :param range_center: The range to the center of the image (m).
%     :param x_image: The x-coordinates of the image (m).
%     :param y_image: The y-coordinates of the image (m).
%     :param z_image: The z-coordinates of the image (m).
%     :param frequency: The frequency array (Hz).
%     :param fft_length: The number of points in the FFT.
%     :return: The reconstructed image.
%
%       Created by: Lee A. Harrison
%       On: 2/9/2019
    
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

    % Loop over all pulses in the data
    term = 1j * 4.0 * pi * frequency(1) / c;
    
    for i = 1:length(sensor_x)
        
        % Calculate the range profile
        range_profile = fftshift(ifft(signal(:, i), fft_length));

        % Calculate the range to each pixel
        range_image = sqrt((sensor_x(i) - x_image) .^ 2 + (sensor_y(i) - y_image) .^ 2 ...
            + (sensor_z(i) - z_image .^ 2)) - range_center;

        % Interpolate the range profile onto the image grid and multiply by the range phase
        % For large scenes, should check the range window and index
        bp_image = bp_image + interp1(range_window, range_profile, range_image, 'linear', 0.0) .* exp(term * range_image);
        
        if rem(i, 100) == 0
            fprintf('%d of %d\n', i, length(sensor_x));
        end
    
    end
end

