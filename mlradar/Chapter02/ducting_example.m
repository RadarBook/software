%% Ducting example
% Created by: Lee A. Harrison
% On: 6/18/2018

clear, clc

% Refractivity gradient (N/km)
refractivity_gradient = linspace(-500, -150, 1000);

% Duct thickness (m)
duct_thickness = [10, 20, 50];

% Calculate the critical angle
critical_angle = ducting(refractivity_gradient, duct_thickness);

% Plot the results
figure; hold on; 
legend_text = [];
for iDuct= 1:numel(duct_thickness)
    plot(refractivity_gradient, critical_angle(iDuct,:));
    legend_text = [legend_text; sprintf('Thickness %.1f (m)', duct_thickness(iDuct))];
end

title('Ducting over a Spherical Earth');
xlabel('Refractivity Gradient (N/km)');
ylabel('Critical Angle (mrad)');
legend(legend_text);
grid on; plot_settings;