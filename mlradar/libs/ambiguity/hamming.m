function [coefficients] = hamming(n)
%% Calculate the coefficients for a Hamming window
%     :param n: number of points in the window.
%     :return: The Hamming window coefficients.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019

i = 0:(n - 1);
coefficients = 0.54 - 0.46 * cos((2.0 * pi * i) / (n - 1));