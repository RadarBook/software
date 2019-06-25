function [ x_db ] = db( x_lin )
%% Convert from linear units to decibels
% :param x_lin: The value in linear units.
% :return: The value in decibels.
%
% Created by: Lee A. Harrison
% On: 6/18/2018

x_db = 10 * log10( x_lin );

end

