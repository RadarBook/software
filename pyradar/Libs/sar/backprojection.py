"""
Project: RadarBook
File: backprojection.py
Created by: Lee A. Harrison
One: 2/9/2019
Created with: PyCharm
"""
from scipy.constants import c, pi
from scipy import sqrt, linspace, zeros_like, exp, sin, cos
from scipy.interpolate import interp1d
from scipy.fftpack import ifft, fftshift


def reconstruct(signal, sensor_x, sensor_y, sensor_z, range_center, x_image, y_image, z_image, frequency, fft_length):
    """
    Reconstruct the two-dimensional image using the filtered backprojection method.
    :param signal: The signal in K-space.
    :param sensor_x: The sensor x-coordinate (m).
    :param sensor_y: The sensor y-coordinate (m).
    :param sensor_z: The sensor z-coordinate (m).
    :param range_center: The range to the center of the image (m).
    :param x_image: The x-coordinates of the image (m).
    :param y_image: The y-coordinates of the image (m).
    :param z_image: The z-coordinates of the image (m).
    :param frequency: The frequency array (Hz).
    :param fft_length: The number of points in the FFT.
    :return: The reconstructed image.
    """
    # Get the frequency step size
    frequency_step = frequency[1] - frequency[0]

    # Calculate the maximum scene size and resolution
    range_extent = c / (2.0 * frequency_step)

    # Calculate the range window for the pulses
    range_window = linspace(-0.5 * range_extent, 0.5 * range_extent, fft_length)

    # Initialize the image
    bp_image = zeros_like(x_image, dtype=complex)

    # Loop over all pulses in the data
    term = 1j * 4.0 * pi * frequency[0] / c

    index = 0
    for xs, ys, zs in zip(sensor_x, sensor_y, sensor_z):

        # Calculate the range profile
        range_profile = fftshift(ifft(signal[:, index], fft_length))

        # Create the interpolation for this pulse
        f = interp1d(range_window, range_profile, kind='linear', bounds_error=False, fill_value=0.0)

        # Calculate the range to each pixel
        range_image = sqrt((xs - x_image) ** 2 + (ys - y_image) ** 2 + (zs - z_image ** 2)) - range_center

        # Interpolate the range profile onto the image grid and multiply by the range phase
        # For large scenes, should check the range window and index
        bp_image += f(range_image) * exp(term * range_image)

        index += 1

    return bp_image


def reconstruct2(signal, sensor_az, sensor_el, x_image, y_image, z_image, frequency, fft_length):
    """
    Reconstruct the two-dimensional image using the filtered backprojection method.
    :param signal: The signal in K-space.
    :param sensor_az: The sensor azimuth positions (rad).
    :param sensor_el: The sensor elevation positions (rad).
    :param x_image: The image x-coordinates (m).
    :param y_image: The image y-coordinates (m).
    :param z_image: The image z-coordinates (m).
    :param frequency: The frequency array (Hz).
    :param fft_length: The number of points in the FFT.
    :return: The reconstructed image.
    """
    # Get the frequency step size
    frequency_step = frequency[1] - frequency[0]

    # Calculate the maximum scene size and resolution
    range_extent = c / (2.0 * frequency_step)

    # Calculate the range window for the pulses
    range_window = linspace(-0.5 * range_extent, 0.5 * range_extent, fft_length)

    # Initialize the image
    bp_image = zeros_like(x_image, dtype=complex)

    # Loop over all pulses in the data
    term = 1j * 4.0 * pi * frequency[0] / c

    index = 0
    for az, el in zip(sensor_az, sensor_el):

        # Calculate the range profile
        range_profile = fftshift(ifft(signal[:, index], fft_length))

        # Create the interpolation for this pulse
        f = interp1d(range_window, range_profile, kind='linear', bounds_error=False, fill_value=0.0)

        # Calculate the range to each pixel
        range_image = x_image * cos(el) * cos(az) + y_image * cos(el) * sin(az) + z_image * sin(el)

        # Interpolate the range profile onto the image grid and multiply by the range phase
        # For large scenes, should check the range window and index
        bp_image += f(range_image) * exp(term * range_image)

        index += 1

    return bp_image


def reconstruct3(signal, az, el, x_image, y_image, z_image, frequency, fft_length):
    """
    Reconstruct the three-dimensional image using the filtered backprojection method.
    :param signal: The signal in K-space.
    :param az: The sensor azimuth positions (rad).
    :param el: The sensor elevation positions (rad).
    :param x_image: The image x-coordinates (m).
    :param y_image: The image y-coordinates (m).
    :param z_image: The image z-coordinates (m).
    :param frequency: The frequency array (Hz).
    :param fft_length: The number of points in the FFT.
    :return: The reconstructed image.
    """
    # Get the frequency step size
    frequency_step = frequency[1] - frequency[0]

    # Calculate the maximum scene size and resolution
    range_extent = c / (2.0 * frequency_step)

    # Calculate the range window for the pulses
    range_window = linspace(-0.5 * range_extent, 0.5 * range_extent, fft_length)

    # Initialize the image
    bp_image = zeros_like(x_image, dtype=complex)

    # Loop over all pulses in the data
    term = 1j * 4.0 * pi * frequency[0] / c

    # Number of rows and columns
    nr, nc = az.shape

    for row in range(nr):
        for col in range(nc):

            # Calculate the range profile
            range_profile = fftshift(ifft(signal[:, row, col], fft_length))

            # Create the interpolation for this pulse
            f = interp1d(range_window, range_profile, kind='linear', bounds_error=False, fill_value=0.0)

            # Calculate the range to each pixel
            range_image = x_image * cos(el[row, col]) * cos(az[row, col]) + \
                          y_image * cos(el[row, col]) * sin(az[row, col]) + \
                          z_image * sin(el[row, col])

            # Interpolate the range profile onto the image grid and multiply by the range phase
            # For large scenes, should check the range window and index
            bp_image += f(range_image) * exp(term * range_image)

    return bp_image
