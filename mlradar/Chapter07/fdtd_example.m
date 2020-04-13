%% FDTD example
% Created by: Lee A. Harrison
% On: 1/15/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
data.mode = 'TM';
data.incident_angle = 90.0; % Degrees
data.number_of_time_steps = 400; 
data.geometry_file = 'fdtd.cell';
data.gaussian_pulse_width = 10; % Steps
data.gaussian_pulse_amplitude = 1.0; 
data.number_of_pml = 20;

% Run the finite difference time domain method
fdtd(data);