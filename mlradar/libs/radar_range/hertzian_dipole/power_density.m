function pd = power_density(relative_permittivity, relative_permeability, frequency, current, element_length, r, theta)
%% Calculate the power density radiated by the Hertzian dipole.
% :param relative_permittivity: The relative permittivity.
% :param relative_permeability: The relative permeability.
% :param frequency: The operating frequency (Hz).
% :param current: The current on the dipole (A).
% :param element_length: The element_length of the dipole (m).
% :param r: The range to the field point (m).
% :param theta: The angle to the field point (radians).
% :return: The power density radiated by the Hertzian dipole (W/m^2).
%
% Created by: Lee A. Harrison
% On: 6/21/2018

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

pd = 0.5 * eta * (k * current * element_length * sin(theta) ./ (4.0 * pi * r)) .^ 2;


end

