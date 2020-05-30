function H = magnetic_field(frequency, current, element_length, r, theta)
%% Calculate the electric far field for the Hertzian dipole.
% :param frequency: The operating frequency (Hz).
% :param current: The current on the dipole (A).
% :param element_length: The element_length of the dipole (m).
% :param r: The range to the field point (m).
% :param theta: The angle to the field point (radians).
%
% Created by: Lee A. Harrison
% On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% The speed of light
c = 299792458; 

% Calculate the angular frequency and material parameters
omega = 2.0 * pi * frequency;

% Calculate the wavenumber
k = omega / c;

% Calculate the magnetic field
H = 1j * k * current * element_length * exp(-1j * k * r) * sin(theta) ./ (4.0 * pi * r);


end

