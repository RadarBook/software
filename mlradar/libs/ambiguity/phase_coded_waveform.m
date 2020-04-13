function [ ambiguity, time_delay, doppler_frequency ] = phase_coded_waveform( code, chip_width )
%% Calculate the ambiguity function for phase coded waveforms.
%     :param code: The value of each chip (1, -1).
%     :param chip_width: The pulsewidth of each chip (s).
%     :return: The ambiguity function.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.


% Upsample factor
n_upsample = 100;

% Number of Doppler bins
n_frequency = 512;

% Code length
n_code = length(code);

% Upsample the code
n_samples = n_upsample * n_code;

% A fast length for the FFT
n_fft_samples = 2^nextpow2(4 * n_samples);

% Initialize the upsampled code
code_up = zeros(n_fft_samples, 1);

for i = 1:n_code
    for j = 1:(n_upsample)
        code_up(n_upsample * (i - 1) + j) = code(i);
    end
end

% Create the FFT of the extended sequence
v = conj(fft(code_up));

% The time delay
s = 0.5 * (n_fft_samples / n_samples);
time_delay = linspace(-n_code * chip_width * s, n_code * chip_width * s, n_fft_samples);

% The Doppler mismatch frequency
doppler_frequency = linspace(-1 / chip_width, 1 / chip_width, n_frequency);

% Initialize the ambiguity function
ambiguity = zeros(n_frequency, n_fft_samples);

% Create the array of FFTs of the shifted sequence
for i = 1:(n_frequency)
    phi = 2.0 * pi * doppler_frequency(i) * time_delay;
    u = fft(code_up .* exp(1j * phi')) .* v;
    ambiguity(i, 1:n_fft_samples) = fftshift(abs(ifft(u, n_fft_samples)));
end

% Normalize the ambiguity function
ambiguity = ambiguity ./ max(max(ambiguity));

ambiguity = ambiguity .^ 2;
