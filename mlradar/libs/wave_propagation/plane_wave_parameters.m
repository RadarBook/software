function pw = plane_wave_parameters(frequency, relative_permittivity, relative_permeability, conductivity)
%% Calculate the parameters from Table 2.2.
% :param frequency: The operating frequency (Hz).
% :param relative_permittivity: The relative permittivity.
% :param relative_permeability: The relative permeability.
% :param conductivity: The conductivity (S).
% :return: The parameters listed in Table 2.2.
%
% Created by: Lee A. Harrison
% On: 6/18/2018

mu_0 = 4 * pi * 1e-7;
epsilon_0 = 8.854187817620389e-12;

% Calculate the angular frequency and material parameters
omega = 2.0 * pi * frequency;
mu = relative_permeability * mu_0;
epsilon = relative_permittivity * epsilon_0;

% Calculate the propagation constant
pw.propagation_constant = 1j * omega .* sqrt(mu .* epsilon) .* sqrt(1 - 1j * conductivity ./ (omega * epsilon));

% Calculate the phase constant
pw.phase_constant = imag(pw.propagation_constant);

% Calculate the attenuation constant
pw.attenuation_constant = real(pw.propagation_constant);

% Calculate the wave impedance
pw.wave_impedance = 1j * omega .* mu ./ pw.propagation_constant;

% Calculate the skin depth
i = pw.attenuation_constant == 0;
pw.skin_depth(i) = 0.0;

i= pw.attenuation_constant ~= 0;
pw.skin_depth(i) = 1. ./ pw.attenuation_constant(i);

% Calculate the wavelength and phase velocity
pw.wavelength = 2. * pi ./ pw.phase_constant;
pw.phase_velocity = omega ./ pw.phase_constant;