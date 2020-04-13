function [ x_db ] = db( x_lin )
%% Convert from linear units to decibels
% :param x_lin: The value in linear units.
% :return: The value in decibels.
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

x_db = 10 * log10( x_lin );

end

