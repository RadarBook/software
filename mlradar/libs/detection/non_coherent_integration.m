function [ pd ] = non_coherent_integration(signal_to_noise, probability_of_false_alarm, number_of_pulses, target_type)
% Calculate the probability of detection for Swerling 0 targets.
%     :param signal_to_noise: The signal to noise ratio.
%     :param probability_of_false_alarm: The probability of false alarm.
%     :param number_of_pulses: The number of pulses to be non-coherently integrated.
%     :param target_type: The Swerling target type (0, 1, 2, 3, or 4).
%     :return: The probability of detection.
%
%     Created by: Lee A. Harrison
%     On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

pd = zeros(1, numel(signal_to_noise));

% Calculate the threshold to noise
threshold_to_noise = threshold_to_noise_ratio(probability_of_false_alarm, number_of_pulses);

if strcmp(target_type, 'Swerling 0')
    
    s = 0;
    
    for n = 2:number_of_pulses
        s = s + (threshold_to_noise ./ (number_of_pulses .* signal_to_noise)) .^ (0.5 * (n - 1.0)) ...
            .* besseli(n-1, 2.0 * sqrt(number_of_pulses .* signal_to_noise * threshold_to_noise));
    end
    if s == inf
        s = realmax;
    end

    for i = 1:length(signal_to_noise)
        pd(i) = Q(sqrt(2.0 * number_of_pulses * signal_to_noise(i)), sqrt(2.0 * threshold_to_noise), 1e-6)...
            + exp(-threshold_to_noise - number_of_pulses * signal_to_noise(i)) * s(i);
    end
    
elseif strcmp(target_type, 'Swerling 1')
    
    pd = 1.0 - gammainc(threshold_to_noise, number_of_pulses - 1) ...
        + (1.0 + 1.0 ./ (number_of_pulses .* signal_to_noise)) .^ (number_of_pulses - 1) ...
        .* gammainc(threshold_to_noise ./ (1.0 + 1.0 ./ (number_of_pulses .* signal_to_noise)), number_of_pulses - 1) ...
        .* exp(-threshold_to_noise ./ (1.0 + number_of_pulses .* signal_to_noise));
    
    
elseif strcmp(target_type, 'Swerling 2')
    
    pd = 1.0 - gammainc(threshold_to_noise ./ (1.0 + signal_to_noise), number_of_pulses);
    
elseif strcmp(target_type, 'Swerling 3')
    
    pd = (1.0 + 2.0 ./ (number_of_pulses * signal_to_noise)) .^ (number_of_pulses - 2) .* ...
        (1.0 + threshold_to_noise ./ (1.0 + 0.5 * number_of_pulses * signal_to_noise)...
        - 2.0 * (number_of_pulses - 2.0) ./ (number_of_pulses * signal_to_noise)) ...
        .* exp(-threshold_to_noise ./ (1.0 + 0.5 * number_of_pulses * signal_to_noise));
    
elseif strcmp(target_type, 'Swerling 4')
    
    s = 0;
    
    for k = 0:number_of_pulses
        s = s + nchoosek(number_of_pulses, k) .* (0.5 * signal_to_noise) .^ -k ...
            .* gammainc(2 * threshold_to_noise ./ (signal_to_noise + 2.0), 2 * number_of_pulses - k);
    end
    
    if s == inf
        s = realmax;
    end
    
    pd = 1.0 - (signal_to_noise ./ (signal_to_noise + 2.0)) .^ number_of_pulses .* s;
end


end

function [ tnr ] =  threshold_to_noise_ratio(probability_of_false_alarm, number_of_pulses)
% Calculate the threshold to noise ratio.
%     :param probability_of_false_alarm: The probability of false alarm.
%     :param number_of_pulses: The number of pulses to be non-coherently integrated.
%     :return: The threshold to noise ratio.

tnr = gammaincinv(1.0 - probability_of_false_alarm, number_of_pulses);

end

