function D = directivity(relative_permittivity, relative_permeability, frequency, current, length, theta)
%% Calculate the directivity for the Hertzian dipole.
%     :param relative_permittivity: The relative permittivity.
%     :param relative_permeability: The relative permeability.
%     :param frequency: The operating frequency (Hz).
%     :param current: The current on the dipole (A).
%     :param length: The length of the dipole (m).
%     :param theta: The angle to the field point (radians).
%     :return: THe directivity of the Hertzian dipole.
%
% Created by: Lee A. Harrison
% On: 6/21/2018

% Get the total radiated power
power_radiated = total_radiated_power(relative_permittivity, relative_permeability, frequency, current, length);

% Calculate the direc
D = 4.0 * pi * radiation_intensity(relative_permittivity, relative_permeability,...
    frequency, current, length, theta) / power_radiated;

end