%% Circular aperture example
% Created by: Lee A. Harrison
% On: 8/3/2018

clear, clc

% Operating frequency (Hz)
frequency = 1.0e9;

% Aperture radius (m)
radius = 0.3;

% Range to the field point (m)
r = 1.0e9;

% Theta and phi angles
n = 200;
m = floor(n/4);
[theta, phi] = meshgrid(linspace(0.0, 0.5 * pi, n), linspace(0.0, 2.0 * pi, n));

% Create a circular TE11 or circular uniform instance
ap = circular_te11_ground_plane(radius, frequency, r, theta, phi);
%ap = circular_uniform_ground_plane(radius, frequency, r, theta, phi);

% Display the parameters
% Beamwidth
[half_power_eplane, half_power_hplane, first_null_eplane, first_null_hplane] = ap.beamwidth;
% fprintf('HPBW Eplane = %.2f (deg)\nHPBW Hplane = %.2f (deg)\nFNBW Eplane = %.2f (deg)\nFNBW Hplane = %.2f (deg)\n', half_power_eplane, half_power_hplane, first_null_eplane, first_null_hplane);

% Directivity
d = ap.directivity;
fprintf('Directivity = %.2f\n', d);

% Sidelobe level
[sll_eplane, sll_hplane] = ap.side_lobe_level;
fprintf('Sidelobe Level Eplane = %.2f (dB)\nSidelobe Level Hplane = %.2f (dB)\n', sll_eplane, sll_hplane);

% Get the far fields
[e_r, e_theta, e_phi, h_r, h_theta, h_phi] = ap.far_fields;

% Calculate the normalized magnitude of the electric field
e_mag = sqrt(abs(e_theta .* e_theta + e_phi .* e_phi));
e_mag = e_mag ./ max(max(e_mag));

% U-V coordinates for plotting the antenna pattern
uu = sin(theta) .* cos(phi);
vv = sin(theta) .* sin(phi);

% Plot the results
figure;
pcolor(uu, vv, abs(e_mag)); shading flat
xlabel('U (sines)');
ylabel('V (sines)');
title('Circular Aperture Antenna Pattern');
axis equal
plot_settings;


figure;
plot(theta(1,:)*180/pi, 2*db(e_mag(m,:))); hold on;
plot(theta(1,:)*180/pi, 2*db(e_mag(1,:))); 
ylim([-60 5]);
title('Circular Aperture Antenna Pattern');
xlabel('Theta (deg)');
ylabel('Normalized |E| (dB)');
legend('E-plane', 'H-plane');
grid on; plot_settings;