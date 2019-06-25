function [ pd ] = coherent_integration(signal_to_noise, number_of_pulses, probability_of_false_alarm, swerling_type)
% Calculate the probability of detection using coherent integration.
%     :param signal_to_noise: The signal to noise ratio.
%     :param number_of_pulses: The number of pulses to be coherently integrated.
%     :param probability_of_false_alarm: The probability of false alarm.
%     :param swerling_type: The Swerling target type (0, 1, or 3).
%     :return: The probability of detection.

%     Created by: Lee A. Harrison
%     On: 10/11/2018

pd = zeros(1, numel(signal_to_noise));

% Calculate the probability of detection based on the Swerling type
if strcmp(swerling_type, 'Swerling 0')
    for i = 1:numel(signal_to_noise)
        pd(i) = Q(sqrt(2.0 * number_of_pulses * signal_to_noise(i)), sqrt(-2.0 * log(probability_of_false_alarm)), 1e-6);
    end
elseif strcmp(swerling_type, 'Swerling 1')
    for i = 1:numel(signal_to_noise)
        pd(i) = exp(log(probability_of_false_alarm) / (number_of_pulses * signal_to_noise(i) + 1.0));
    end
elseif strcmp(swerling_type, 'Swerling 3')
    for i = 1:numel(signal_to_noise)
        pd(i) = (1.0 - (2.0 * number_of_pulses * log(probability_of_false_alarm)) / ...
            (2.0 + number_of_pulses * signal_to_noise(i)) ^ 2) * exp((2.0 * log(probability_of_false_alarm)) / ...
            (2.0 + number_of_pulses * signal_to_noise(i)));
    end
end


end

