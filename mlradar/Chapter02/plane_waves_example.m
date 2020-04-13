%% Plane waves example
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Operating frequency (Hz)
frequency = 300e6;

% Relative permittivity
relative_permittivity = 4.3;

% Relative permeability
relative_permeability = 1.0;

% Conductivity (S/m)
conductivity = 0.01;

% Get the plane wave parameters for Table 2.2
pw = plane_wave_parameters(frequency, relative_permittivity, relative_permeability, conductivity);

% Display the plane wave parameters
fprintf('Propagation Constant = %.2f + %.2fj (1/m)\n', real(pw.propagation_constant), imag(pw.propagation_constant));
fprintf('Attenuation Constant = %.2f (Np/m)\n', pw.attenuation_constant);
fprintf('Phase Constant = %.2f (rad/m)\n', pw.phase_constant);
fprintf('Wave Impedance = %.2f + %.2fj (Ohms)\n', real(pw.wave_impedance), imag(pw.wave_impedance));
fprintf('Skin Dpeth = %.2f (m)\n', pw.skin_depth);
fprintf('Wavelength = %.2f (m)\n', pw.wavelength);
fprintf('Phase Velocity = %.2f (m/s)\n', pw.phase_velocity);

%% Plot the electric and magnetic fields

% Determine 2 lambda distance for plotting
z = linspace(0, 2.0 * 3e8 / frequency, 1000);

% Retrieve the plane wave parameters
gamma = pw.propagation_constant;
eta = pw.wave_impedance;

% Set up the angular frequency
omega = 2.0 * pi * frequency;

% Set up the time
time = 0 / omega * 0.1;

% Calculate the electric and magnetic fields
exp_term = exp(-gamma * z) * exp(1j * omega * time);
Ex = real(exp_term);
Hy = real(exp_term / eta);

% Plot the electric and magentic fields
figure; hold on
[ax, h1, h2] = plotyy(z, Ex, z, Hy); 
xlabel('Distance (m)');
title('Uniform Plane Wave');
grid on; plot_settings;

% Use the axis handles to set the labels of the y axes
set(get(ax(1), 'Ylabel'), 'String', 'Electric Field (V/m)');
set(get(ax(2), 'Ylabel'), 'String', 'Magnetic Field (A/m)');