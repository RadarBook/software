function theta_apparent = apparent_elevation_approximate(theta_true, height)
%% Calculate the apparent elevation angle with the approximate equation.
% :param theta_true: The true elevation angle (degrees).
% :param height: The height of the radar (km).
% :return: The approximated apparent elevation angle (degrees).
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

angle_correction = 1. / (1.728 + 0.5411 * theta_true + 0.03723 * theta_true^2 + ...
    height * (0.1815 + 0.06272 * theta_true + 0.01380 * theta_true^2) + height^2 * (0.01727 + 0.008288 * theta_true));

theta_apparent = theta_true + angle_correction;