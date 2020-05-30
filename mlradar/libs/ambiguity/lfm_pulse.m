function [ ambiguity ] = lfm_pulse(time_delay, doppler_frequency, pulse_width, bandwidth)
%% Calculate the ambiguity function for a linear frequency modulated single pulse.
%     :param time_delay: The time delay for the ambiguity function (seconds)
%     :param doppler_frequency: The Doppler frequency for the ambiguity function (Hz)
%     :param pulse_width: The waveform pulse width (seconds)
%     :param bandwidth: The waveform band width (Hz)
%     :return: The ambiguity function for an LFM pulse (unitless)
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

ambiguity = abs((1.0 - abs(time_delay) / pulse_width) .* sinc(pi * pulse_width .*...
    (bandwidth / pulse_width * time_delay + doppler_frequency) .* (1.0 - abs(time_delay) / pulse_width))).^2;

if length(time_delay) == 1 && abs(time_delay) > pulse_width
    ambiguity(:) = 0;
else
    ambiguity(abs(time_delay) > pulse_width) = 0;
end