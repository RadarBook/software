function [ in_phase, quadrature ] = coherent_detector(if_signal, center_frequency, bandwidth, sample_frequency, time)
%% Calculate the baseband I and Q signals from the IF signal.
%     :param if_signal: The input IF signal to the detector.
%     :param center_frequency: The center frequency of the IF signal (Hz).
%     :param bandwidth: The bandwidth of the IF signal (Hz).
%     :param sample_frequency: The sampling rate (Hz).
%     :param time: The time vector for the IF signal (s).
%     :return: The baseband I and Q signals.
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Shift the IF signal to baseband by mixing with the oscillator frequency
in_phase = if_signal .* exp(-1j * 2.0 * pi * center_frequency * time);
quadrature = if_signal .* exp(-1j * (2.0 * pi * center_frequency * time + 0.5 * pi));

% Calculate the spectra
frequencies = fftfreq(round(sample_frequency), 1.0 / sample_frequency);
i_freq = fft(in_phase);
q_freq = fft(quadrature);

% Use 6th order Butterworth low pass filter
[zb, pb, kb] = butter(6, 2.0 * pi * (0.5 * bandwidth), 'low');
[b, a] = zp2tf(zb, pb, kb);
[h, w] = freqs(b, a, frequencies * pi / 180.);

i_freq = i_freq * h;
q_freq = q_freq * h;

% Calculate the time domain I/Q of the signal
in_phase = ifft(i_freq);
quadrature = ifft(q_freq);

end

