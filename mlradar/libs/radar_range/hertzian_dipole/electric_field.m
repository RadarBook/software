function E = electric_field( relative_permittivity, relative_permeability, frequency, current, element_length, r, theta )
%% Calculate the electric far field for the Hertzian dipole.
% :param relative_permittivity: The relative permittivity.
% :param relative_permeability: The relative permeability.
% :param frequency: The operating frequency (Hz).
% :param current: The current on the dipole (A).
% :param element_length: The element_length of the dipole (m).
% :param r: The range to the field point (m).
% :param theta: The angle to the field point (radians).
% :return: The electric far field for the Hertzian dipole (theta-hat) (V/m).
%
% Created by: Lee A. Harrison
% On: 6/21/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Permeability and permittivity
mu_0 = 4 * pi * 1e-7;
epsilon_0 = 8.854187817620389e-12;

% The speed of light
c = 299792458; 

% Calculate the angular frequency and material parameters
omega = 2.0 * pi * frequency;
mu = relative_permeability * mu_0;
epsilon = relative_permittivity * epsilon_0;

% Calculate the wavenumber
k = omega / c;

% Calculate the impedance
eta = sqrt(mu / epsilon);

% Calculate the electric field
E = 1j * eta * k * current * element_length * exp(-1j * k * r) * sin(theta) ./ (4.0 * pi * r);

end