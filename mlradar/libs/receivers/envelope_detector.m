function y = envelope_detector( if_signal )
%%     Calculate the amplitude envelope of the IF signal.
%     :param if_signal: The signal at IF.
%     :return: The amplitude envelope.
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

n = length(if_signal);
X = fft(if_signal, n);
h = zeros(1, n);
h(1) = 1;
h(2:n/2 + 1) = 2.0 * ones(1, n/2);
h(n/2 + 1) = 1;
Z = X.*h;
y = abs((ifft(Z, n)));


end

