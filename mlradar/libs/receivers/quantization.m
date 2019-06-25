function [ quantized_signal, error_signal ] = quantization(if_signal, number_of_bits)
%% Calculate the quantized signal for a given number of bits.
%     :param if_signal: The sampled analog signal to be quantized.
%     :param number_of_bits: The number of bits in the ADC.
%     :return: The quantized signal.
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018

% Calculate the LSB level
lsb = 2.0 / (2.0 ^ number_of_bits - 1);

% Calculate the quantized signal
quantized_signal = lsb * round((if_signal + 1.0) / lsb) - 1.0;

% Calculate the error between the analog signal and the quantized signal
error_signal = if_signal - quantized_signal;


