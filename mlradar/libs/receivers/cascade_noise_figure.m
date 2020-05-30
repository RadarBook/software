function total_nf = cascade_noise_figure(gain, noise_figure)
%% Calculate the total noise figure for a cascaded network.
%     :param gain: The gain of each component (dB).
%     :param noise_figure: The noise figure of each component (dB).
%     :return: The total noise figure (dB).
%
%     Created by: Lee A. Harrison
%     On: 9/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

    % Convert noise figure and gain to linear units
    noise_factor = 10.0 .^ (noise_figure / 10.0);
    gain_linear = 10.0 .^ (gain / 10.0);

    % Start with the first component
    total = noise_factor(1);

    % Loop over the remaining components
    for i = 2:length(noise_factor)
        total = total + (noise_factor(i) - 1.0) / prod(gain_linear(1:i-1));
    end

    % Return the total noise figure
    total_nf = 10.0 * log10(total);
end

