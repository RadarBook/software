%% Reflection and transmission example
% Created by: Lee A. Harrison
% On: 6/18/2018

clear, clc

% Operating frequency (Hz)
frequency = 300e6;

% Material 1
relative_permittivity(1) = 1.3;
relative_permeability(1) = 1.0;
conductivity(1) = 0.01;

% Material 2
relative_permittivity(2) = 2.8;
relative_permeability(2) = 1.0;
conductivity(2) = 0.01;

% Calculate the critical angle and Brewster angle
theta_c = critical_angle(frequency, relative_permittivity, relative_permeability, conductivity);
theta_b = brewster_angle(frequency, relative_permittivity, relative_permeability, conductivity);

fprintf('Critical Angle = %.2f + %.2fj (deg)\n', real(theta_c), imag(theta_c));
fprintf('Brewster Angle = %.2f + %.2fj (deg)\n', real(theta_b), imag(theta_b));

% Set the incident angle
incident_angle = linspace(0, 0.5 * pi, 1000);

% Calculate the reflection and transmission coefficients
pw = reflection_transmission(frequency, incident_angle, relative_permittivity, relative_permeability, conductivity);

% Plot the reflection coefficients
figure; 
subplot(211)
plot(rad2deg(incident_angle), abs(pw.reflection_coefficient_te), 'b');hold on
plot(rad2deg(incident_angle), abs(pw.reflection_coefficient_tm), 'b--');
title('Reflection Coefficients');
xlabel('Incident Angle (degrees)');
ylabel('|Reflection Coefficient|');
legend({'|\Gamma_T_E|', '|\Gamma_T_M|'});
grid on; plot_settings;

% Plot the transmission coefficients
subplot(212)
plot(rad2deg(incident_angle), abs(pw.transmission_coefficient_te), 'r');hold on
plot(rad2deg(incident_angle), abs(pw.transmission_coefficient_tm), 'r--');
title('Transmission Coefficients');
xlabel('Incident Angle (degrees)');
ylabel('|Transmission Coefficient|');
legend({'|T_T_E|', '|T_T_M|'});
grid on; plot_settings;