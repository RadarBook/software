function total_power = total_radiated_power(relative_permittivity, relative_permeability, frequency, current, element_length)
%% Calculate the total power radiated by the Hertzian dipole.
% :param relative_permittivity: The relative permittivity.
% :param relative_permeability: The relative permeability.
% :param frequency: The operating frequency (Hz).
% :param current: The current on the dipole (A).
% :param element_length: The element_length of the dipole (m).
% :return: The total power radiated byt the Hertzian dipole (W).
%
% Created by: Lee A. Harrison
% On: 6/21/2018

% Permeability and permittivity
mu_0 = 4 * pi * 1e-7;
epsilon_0 = 8.854187817620389e-12;

% The speed of light
c = 299792458; 

% Calculate the material parameters
mu = relative_permeability * mu_0;
epsilon = relative_permittivity * epsilon_0;

% Calculate the wavelength
wavelength = c / frequency;

% Calculate the impedance
eta = sqrt(mu / epsilon);

% Calculate the total power radiated
total_power = eta * pi / 3.0 * (current * element_length / wavelength) ^ 2;

end

