function [ x_lin ] = lin( x_db )
%% Convert from decibels to linear units
% :param x_db: The value in decibels.
% :return: The value in linear units.
%
% Created by: Lee A. Harrison
% On: 6/18/2018

x_lin = 10 .^ (x_db ./ 10);

end

