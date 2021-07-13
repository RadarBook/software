%% Stratified sphere example
% Created by: Lee A. Harrison
% On: 1/18/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
frequency = 1e9; % Hz
radius = [1.0, 1.25]; % meters
mu_r = [1.0, 1.0];
eps_r = [1.0, 4.0];
number_of_modes = 60;

pec_core = true;

% To put the parameters in order
nr = numel(radius);

mu = ones(nr + 1, 1);
eps = ones(nr + 1, 1);
ra = ones(nr, 1);

% Set up the parameters in the correct order

for ir = 1:nr
    ra(nr + 1 - ir) = radius(ir);
end

for ie = 1:numel(eps_r)
    mu(nr + 2 - ie) = mu_r(ie);
    eps(nr + 2 - ie) = eps_r(ie);
end

% Set the observation angles
observation_angle = linspace(0, pi, 721);

[An, Bn] = sphere_coefficients(frequency, eps, mu, ra, number_of_modes, pec_core);

for i = 1:numel(observation_angle)
    [et(i), ~] = stratified_sphere(frequency, observation_angle(i), 0, An, Bn);
    [~, ep(i)] = stratified_sphere(frequency, observation_angle(i), 0.5 * pi, An, Bn);
end        

% Display the results
figure;
plot(observation_angle * 180 / pi, 20 * log10(abs(ep))); hold on
plot(observation_angle * 180 / pi, 20 * log10(abs(et)))
title('RCS vs Bistatic Angle')
ylabel('RCS (dBsm)')
xlabel('Observation Angle (deg)')

ylim([min(20.0 * log10(abs(et))) - 3, max(20.0 * log10(abs(et))) + 3])

% Legend
legend({'TE', 'TM'})

% Turn on the grid
grid on

% Plot settings
plot_settings;