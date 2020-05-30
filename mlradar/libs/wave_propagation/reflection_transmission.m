function pw2 = reflection_transmission(frequency, incident_angle, relative_permittivity, relative_permeability, conductivity)
%% Calculate the reflection and transmission coefficients.
% :param frequency:  The operating frequency (Hz).
% :param incident_angle: The incident angle (radians).
% :param relative_permittivity: The relative permittivty.
% :param relative_permeability: The relative permeability.
% :param conductivity: The conductivity (S).
% :return: The reflection and transmission coefficients.
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Get the wave impedance and propagation constant for each material
pw = plane_wave_parameters(frequency, relative_permittivity, relative_permeability, conductivity);

% Calculate the transmission angle
transmission_angle = asin(pw.propagation_constant(1) / pw.propagation_constant(2) .* sin(incident_angle));

% Calculate the transmission and reflection coefficients for the TE polarization
reflection_coefficient_te = (pw.wave_impedance(2) .* cos(incident_angle) - pw.wave_impedance(1) .* cos(transmission_angle)) ./ ...
    (pw.wave_impedance(2) .* cos(incident_angle) + pw.wave_impedance(1) .* cos(transmission_angle));

transmission_coefficient_te = (2. * pw.wave_impedance(2) .* cos(incident_angle)) ./ ...
    (pw.wave_impedance(2) .* cos(incident_angle) + pw.wave_impedance(1) .* cos(transmission_angle));

% Calculate the transmission and reflection coefficients for the TM polarization
reflection_coefficient_tm = (pw.wave_impedance(2) .* cos(transmission_angle) - pw.wave_impedance(1) .* cos(incident_angle)) ./ ...
    (pw.wave_impedance(2) .* cos(transmission_angle) + pw.wave_impedance(1) .* cos(incident_angle));

transmission_coefficient_tm = (2. * pw.wave_impedance(2) .* cos(incident_angle)) ./ ...
    (pw.wave_impedance(2) .* cos(transmission_angle) + pw.wave_impedance(1) .* cos(incident_angle));

pw2.reflection_coefficient_te = reflection_coefficient_te;
pw2.transmission_coefficient_te = transmission_coefficient_te;
pw2.reflection_coefficient_tm = reflection_coefficient_tm;
pw2.transmission_coefficient_tm = transmission_coefficient_tm;