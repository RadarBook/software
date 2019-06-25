function theta_apparent = apparent_elevation(theta_true, height)
%% Calculate the apparent elevation of the target.
% :param theta_true: The true elevation angle (degrees).
% :param height: The height of the radar (km).
% :return: The apparent elevation angle of the target (degrees).
%
% Created by: Lee A. Harrison
% On: 6/18/2018

theta_apparent = theta_true - 180/pi * integral(@integrand, height, 1000);

    function dz = integrand(z)        
        %% Determine the integrand for calculating the apparent elevation angle
        % :param z: The altitude (km).
        % :return: The integrand.
        
        % Effective radius of the Earth (km)
        re = 6378.137;
        
        % Standard values
        a = 0.000315;
        b = 0.1361;
        
        % Refractive index and derivative as a function of altitude
        n_z = 1. + a * exp(-b * z);
        np_z = -(a * b * exp(-b * z));
        
        % Refractive index at the given height
        n_h = 1. + a * exp(-b * height);
        
        tan_phi = tan(acos(((re + height) * n_h) ./ ((re + z) .* n_z) .* cos(theta_true * pi/180)));
        
        dz = np_z ./ (n_z .* tan_phi);
    end

end