function critical_angle = ducting(refractivity_gradient, duct_thickness)
%% Calculate the critical angle for ducting.
% :param refractivity_gradient: The refractivity gradient (N/km).
% :param duct_thickness: The duct thickness (meters).
% :return: The critical angle for ducting to occur (radians).
%
% Created by: Lee A. Harrison
% On: 6/18/2018

for iDuct = 1:numel(duct_thickness)
    critical_angle(iDuct,:) = sqrt(2.e-6 * abs(refractivity_gradient) * duct_thickness(iDuct) * 1e-3);
end