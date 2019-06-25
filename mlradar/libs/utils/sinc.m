function [ s ] = sinc( x )
%% Calculate the sinc function
% :param x: Argument of the sinc function.
% :return: The value of sinc(x).
%
% Created by: Lee A. Harrison
% On: 6/18/2018

s = ones(size(x));
index = x ~= 0.0;
s(index) = sin(pi * x(index)) ./ (pi * x(index));

end

