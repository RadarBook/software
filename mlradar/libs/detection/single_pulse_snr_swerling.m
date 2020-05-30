function [ signal_to_noise ] = single_pulse_snr_swerling(pd, pfa, number_of_pulses, swerling_type)
% Compute the required signal to noise ratio given a probability of detection and probability of false alarm.
%     :param pd: The probability of detection.
%     :param pfa: The probability of false alarm.
%     :param number_of_pulses: The number of pulses to be integrated.
%     :param swerling_type: The Swerling model type.
%     :return: The required signal to noise ratio.

%     Created by: Lee A. Harrison
%     On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

signal_to_noise = 1.0;
delta = 1000.0;

while 1
    if pd > non_coherent_integration(signal_to_noise, pfa, number_of_pulses, swerling_type);
        signal_to_noise = signal_to_noise + delta;
    else
        signal_to_noise = signal_to_noise - delta;
    end
    
    if signal_to_noise < 0.0
        signal_to_noise = 1e-6;
    end
    
    delta = 0.5 * delta;
    
    if abs(pd - non_coherent_integration(signal_to_noise, pfa, number_of_pulses, swerling_type)) < 1e-6
        break;
    end
end

end

