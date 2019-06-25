function [ pd ] = pd_gaussian(signal_to_noise, probability_false_alarm)
% Calculate the probability of detection for a given signal to noise ratio and probability of false alarm
%     when the noise is Gaussian (non-coherent detection).
%     :param signal_to_noise: The signal to noise ratio.
%     :param probability_false_alarm: The probability of false alarm.
%     :return: The probability of detection.

%     Created by: Lee A. Harrison
%     On: 10/11/2018

% Calculate the voltage threshold
voltage_threshold = erfinv(1.0 - 2.0 * probability_false_alarm) * sqrt(2.0);

% Calculate the signal amplitude based on signal to noise ratio
amplitude = sqrt(2.0 * signal_to_noise);

% Calculate the probability of detection
pd = 0.5 * (1.0 - erf((voltage_threshold - amplitude) / sqrt(2.0)));


end

