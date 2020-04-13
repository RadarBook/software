%% Optimum binary example
% Created by: Lee A. Harrison
% On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Gaussian pdf
x = -3:0.01:3;
y = pdf('Normal', x, 1.0, 2.0);

% Weibull
pd = makedist('Weibull','a',5,'b',2);
x = 0:0.01:15;
y = pdf(pd, x);

% Rayleigh
x = 0:0.01:2;
y = raylpdf(x, 0.5);

% Rician
x = 0:0.01:10;
pd = makedist('Rician','s',0,'sigma',2);
y = pdf(pd, x);

% Chi-Squared
x = 0:0.01:15;
y = chi2pdf(x, 4);

% Plot the results
figure;
plot(x, y);
title('Probability Density Function');
xlabel('x');
ylabel('Probability p(x)');
grid on;
plot_settings;