function theta = brewster_angle(frequency, relative_permittivity, relative_permeability, conductivity)
%% Calculate the Brewster angle.
% :param frequency: The operating frequency (Hz).
% :param relative_permittivity: The relative permittivty.
% :param relative_permeability: The relative permeability.
% :param conductivity: The conductivity (S).
% :return: The Brewster angle (radians).
%
% Created by: Lee A. Harrison
% On: 6/18/2018

% Get the wave impedance and propagation constant for each material
pw = plane_wave_parameters(frequency, relative_permittivity, relative_permeability, conductivity);

term1 = (pw.wave_impedance(1) / pw.wave_impedance(2))^2;

term2 = (pw.propagation_constant(1) / pw.propagation_constant(2))^2;

theta = asin(sqrt((term1 - 1.) / (term1 - term2))) * 180. / pi;