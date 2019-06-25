%% Hertzian dipole example
% Created by: Lee A. Harrison
% On: 7/1/2018

clear, clc

% The relative permittivity
relative_permittivity = 1.3;

% The relative permeability
relative_permeability = 1.0;

% The operating frequency (Hz)
frequency = 1.0e9;

% The current on the dipole (A)
current = 1.0;

% The dipole length (m)
element_length = 0.01;

% The range to the field point (m)
r = 10.0e3;

% Full angle sweep
theta = linspace(0, 2*pi, 1000);

% Calculate the electric field
E = electric_field( relative_permittivity, relative_permeability, frequency, current, element_length, r, theta );

% Calculate the magnetic field
H = magnetic_field(frequency, current, element_length, r, theta);

% Calculate the power density
pd = power_density(relative_permittivity, relative_permeability, frequency, current, element_length, r, theta);

% Calculate the radiation intensity
U = radiation_intensity(relative_permittivity, relative_permeability, frequency, current, element_length, theta);

% Calculate the directivity
D = directivity(relative_permittivity, relative_permeability, frequency, current, element_length, theta);

% Calculate the total radiated power
total_power = total_radiated_power(relative_permittivity, relative_permeability, frequency, current, element_length);

% Plot the electric field
figure;
polar(theta, abs(E));
title('Hertzian Dipole Electric Field (V/m)');
plot_settings;

% Plot the magenetic field
figure;
polar(theta, abs(H));
title('Hertzian Dipole Magnetic Field (A/m)');
plot_settings;

% Plot the power density
figure;
polar(theta, pd);
title('Hertzian Dipole Power Density (W/m^{2})');
plot_settings;

% Plot the radiation intensity
figure;
polar(theta, U);
title('Hertzian Dipole Radiation Intensity');
plot_settings;

% Plot the directivity
figure;
polar(theta, D);
title('Hertzian Dipole Directivity');
plot_settings;

% Display the total radiated power
fprintf('Total radiated power = %.2f (W)\n', total_power);