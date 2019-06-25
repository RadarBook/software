function [coefficients] = kaiser(n, alpha)
%% Calculate the coefficients for a Kaiser window
%     :param n: number of points in the window.
%     :param alpha: sidelobe parameter.
%     :return: The Hamming window coefficients.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019

i = 0:(n - 1);

z1 = pi * alpha * sqrt(1.0 - (2.0 * i / (n - 1) - 1).^2);

z2 = pi * alpha;

coefficients = besseli(0,z1) ./ besseli(0,z2);