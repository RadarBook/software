%% Optimum binary example
% Created by: Lee A. Harrison
% On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
number_of_pulses = 10;
target_type = 'Swerling 0';

if strcmp(target_type, 'Swerling 0')
    alpha = 0.8;
    beta = -0.02;
elseif strcmp(target_type, 'Swerling 1')
    alpha = 0.8;
    beta = -0.02;
elseif strcmp(target_type, 'Swerling 2')
    alpha = 0.91;
    beta = -0.38;
elseif strcmp(target_type, 'Swerling 3')
    alpha = 0.8;
    beta = -0.02;
elseif strcmp(target_type, 'Swerling 4')
    alpha = 0.873;
    beta = -0.27;
end

% Calculate the optimum choice for M
n = 1:number_of_pulses + 1;
m_optimum = ceil(10.0 ^ beta * n .^ alpha);

% Plot the results
figure;
plot(n, m_optimum);
title('Optimum M for Binary Integration');
xlabel('Number of Pulses');
ylabel('M');
grid on;
plot_settings;