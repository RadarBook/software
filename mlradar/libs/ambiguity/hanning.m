function [coefficients] = hanning(n)
%% Calculate the coefficients for a Hanning window
%     :param n: number of points in the window.
%     :return: The Hanning window coefficients.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019

i = 0:(n - 1);
coefficients = 0.5 - 0.5 * cos((2.0 * pi * i) / (n - 1));