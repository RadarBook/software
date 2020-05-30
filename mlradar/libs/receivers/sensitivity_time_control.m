function [ receive_range, attenuation ] = sensitivity_time_control(pulse_repetition_frequency, pulse_width)
%% Calculate the STC attenuation.
%     :param pulse_repetition_frequency: The PRF (Hz).
%     :param pulse_width: The pulse width (s).
%     :return: The normalized STC attenuation.
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Speed of light (m/s)
c = 299792458;

% Calculate the PRI
pulse_repetition_interval = 1.0 / pulse_repetition_frequency;

% Find the minimum and maximum ranges
minimum_range = 0.5 * c * pulse_width;
maximum_range = 0.5 * c * pulse_repetition_interval;

% Set up the range array
receive_range = linspace(0, maximum_range, 1000);

% Calculate and return the attenuation
attenuation = 1.0 ./ receive_range .^ 3.5;
attenuation(receive_range < minimum_range) = 1.0 ./ minimum_range .^ 3.5;

end

