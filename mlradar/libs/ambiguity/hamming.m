function [coefficients] = hamming(n)
%% Calculate the coefficients for a Hamming window
%     :param n: number of points in the window.
%     :return: The Hamming window coefficients.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

i = 0:(n - 1);
coefficients = 0.54 - 0.46 * cos((2.0 * pi * i) / (n - 1));