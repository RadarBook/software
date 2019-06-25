function [ signal_to_noise ] = single_pulse_snr(probability_of_detection, probability_of_false_alarm)
% Calculate the required signal to noise ratio given a probability of detection and probability of false alarm.
%     :param probability_of_detection: The probability of detection.
%     :param probability_of_false_alarm: The probability of false alarm.
%     :return: The required signal to noise ratio.
%
%     Created by: Lee A. Harrison
%     On: 10/11/2018


% Starting values
signal_to_noise = 1.0;
delta = 100.0;

% Loop until required SNR is found
while 1
    if probability_of_detection > pd_rayleigh(signal_to_noise, probability_of_false_alarm);
        signal_to_noise = signal_to_noise + delta;
    else
        signal_to_noise = signal_to_noise - delta;
    end
    
    delta = 0.5 * delta;
    
    if abs(probability_of_detection - pd_rayleigh(signal_to_noise, probability_of_false_alarm)) < 1e-6
        break
    end
end


end