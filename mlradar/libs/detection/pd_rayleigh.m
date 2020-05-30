function [ pd ] = pd_rayleigh(signal_to_noise, probability_false_alarm)
% Calculate the probability of detection for a given signal to noise ratio and probability of false alarm
%     when the noise is Rayleigh (coherent detection).
%     :param signal_to_noise: The signal to noise ratio.
%     :param probability_false_alarm: The probability of false alarm.
%     :return: The probability of detection.
%
%     Created by: Lee A. Harrison
%     On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

pd = zeros(1, length(signal_to_noise));

% Calculate the probability of detection
for i = 1:length(signal_to_noise)
    pd(i) = Q(sqrt(2.0 * signal_to_noise(i)), sqrt(-2.0 * log(probability_false_alarm)), 1e-6);
end

end

