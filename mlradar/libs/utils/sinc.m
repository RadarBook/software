function [ s ] = sinc( x )
%% Calculate the sinc function
% :param x: Argument of the sinc function.
% :return: The value of sinc(x).
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

s = ones(size(x));
index = x ~= 0.0;
s(index) = sin(pi * x(index)) ./ (pi * x(index));

end

