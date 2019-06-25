function y = envelope_detector( if_signal )
%%     Calculate the amplitude envelope of the IF signal.
%     :param if_signal: The signal at IF.
%     :return: The amplitude envelope.
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018
%

n = length(if_signal);
X = fft(if_signal, n);
h = zeros(1, n);
h(1) = 1;
h(2:n/2 + 1) = 2.0 * ones(1, n/2);
h(n/2 + 1) = 1;
Z = X.*h;
y = abs((ifft(Z, n)));


end

