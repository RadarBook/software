function theta = critical_angle(frequency, relative_permittivity, relative_permeability, conductivity)
%% Calculate the critical angle for total reflection.
% :param frequency: The operating frequency (Hz).
% :param relative_permittivity: The relative permittivty.
% :param relative_permeability: The relative permeability.
% :param conductivity: The conductivity (S).
% :return: The critical angle (radians).
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Get the wave impedance and propagation constant for each material
pw = plane_wave_parameters(frequency, relative_permittivity, relative_permeability, conductivity);

theta = asin(pw.propagation_constant(2) / pw.propagation_constant(1)) * 180. / pi;