function [ snr ] = snr_reduction(number_of_pulses, signal_to_noise_nci)
% Calculate the required single pulse signal to noise for non-coherent integration (loss method Curry).
%     :param number_of_pulses: The number of pulses to be non-coherently integrated.
%     :param signal_to_noise_nci: The signal to noise ratio for non-coherent integration.
%     :return: The required single pulse signal to noise ratio.
% 
%     Created by: Lee A. Harrison
%     On: 10/11/2018
    
    snr = 10.0 * log10(signal_to_noise_nci ./ (2.0 * number_of_pulses) + ...
           sqrt(signal_to_noise_nci .^ 2 ./ (4.0 * number_of_pulses .^ 2) + signal_to_noise_nci ./ number_of_pulses));

end

