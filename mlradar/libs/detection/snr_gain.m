function [ snr ] = snr_gain(probability_of_detection, probability_of_false_alarm, number_of_pulses, signal_to_noise_nci)
% Calculate the required single pulse signal to noise for non-coherent integration (gain method Peebles).
%     :param probability_of_detection: The probability of detection.
%     :param probability_of_false_alarm: The probability of false alarm.
%     :param number_of_pulses: The number of pulses to be non-coherently integrated.
%     :param signal_to_noise_nci: The signal to noise ratio for non-coherent integration.
%     :return: The requried single pulse signal to noise ratio.
%     
%     Created by: Lee A. Harrison
%     On: 10/11/2018

    gain = 6.79 * (1.0 + 0.235 * probability_of_detection) * (1.0 + log10(1.0/probability_of_false_alarm) / 46.6)...
           .* log10(number_of_pulses) .* (1.0 - 0.14 * log10(number_of_pulses) + 0.01831 * log10(number_of_pulses) .^ 2);

    snr = 10.0 * log10(signal_to_noise_nci) - gain;

end

