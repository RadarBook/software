function [coefficients] = kaiser(n, alpha)
%% Calculate the coefficients for a Kaiser window
%     :param n: number of points in the window.
%     :param alpha: sidelobe parameter.
%     :return: The Hamming window coefficients.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

i = 0:(n - 1);

z1 = pi * alpha * sqrt(1.0 - (2.0 * i / (n - 1) - 1).^2);

z2 = pi * alpha;

coefficients = besseli(0,z1) ./ besseli(0,z2);