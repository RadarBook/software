function [ code ] = n_phase_code( n )
%% Generate an N-phase Frank code sequence.
%     :param n: The sequence groups.
%     :return: The Frank code sequence (length N^2).
% 
%     Created by: Lee A. Harrison
%     On: 4/26/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

phi = zeros(n ^ 2, 1);

for i = 1:n
    for j = 1:n
        phi((i - 1) * n + j) = 2.0 * pi / n * (i - 1) * (j - 1);
    end
end

code = exp(1j * phi);