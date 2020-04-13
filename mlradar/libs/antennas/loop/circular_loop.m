classdef circular_loop
    % Circular loop antenna
    % Created by: Lee A. Harrison
    % On: 8/1/2018
    %
    % Copyright (C) 2019 Artech House (artech@artechhouse.com)
    % This file is part of Introduction to Radar Using Python and MATLAB
    % and can not be copied and/or distributed without the express permission of Artech House.
    
    properties
        % Circular loop antenna properties
        radius = 1.0;  % The loop radius (m).
        current = 1.0; % The dipole current (A).
        frequency = 1.0e9; % The operating frequency (Hz).
        r = 1.0e9; % The distance to the field point (m).
        theta = 2.0 * pi; % The angle to the field point (rad).
    end
    
    methods
        % Methods for circular loop antenna
        function obj = circular_loop(radius, current, frequency, r, theta)
            % Class constructor
            if(nargin > 0)
                obj.radius = radius;
                obj.current = current;
                obj.frequency = frequency;
                obj.r = r;
                obj.theta = theta;
            end
        end
        
        function d = directivity(obj)
            % The directivity of a circular loop antenna.
            % :param frequency: The operating frequency (Hz).
            % :param radius: The radius of the loop antenna (m).
            % :return: The directivity.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            d = 2.0 * k * obj.radius * 0.58 ^ 2;
        end
        
        
        function b = beamwidth(obj)
            % The half power beamwidth of a circular loop antenna.
            % :param frequency: The operating frequency (Hz).
            % :param radius: The radius of the circular loop (m).
            % :return: The beamwidth (deg).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi *obj. frequency / c;
            
            % Calculate the normalized radiation intensity
            theta = linspace(eps, pi, 10000);
            f = besselj(1, k * obj.radius * sin(theta)) .^ 2;
            g = f ./ max(f);
            
            for iTheta = 1:numel(theta)
                if g(iTheta) >= 0.5
                    theta_half = 0.5 * pi - theta(iTheta);
                    break;
                end
            end
            
            b = 2.0 * theta_half * 180.0 / pi;
        end
        
        
        function ae = maximum_effective_aperture(obj)
            % Calculate the maximum effective aperture of an circular loop antenna.
            % :param radius: The radius of the loop antenna (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The maximum effective aperture (m^2).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the wavenumber
            k = 2.0 * pi / wavelength;
            
            ae = k * obj.radius * wavelength ^ 2 / (4.0 * pi) * 0.58 ^ 2;
        end
        
        
        function r = radiation_resistance(obj)
            % Calculate the radiation resistance for a small circular loop.
            % :param frequency: The operating frequency (Hz).
            % :param radius: The radius of the small circular loop (m).
            % :return: The radiation resistance (Ohms).
            
            % Speed of light
            c = 299792458;
            
            % Calculate and return the radiation resistance
            r = 60.0 * pi ^ 2 * 2.0 * pi * obj.frequency / c * obj.radius;
        end
        
        
        function r = radiated_power(obj)
            % Calculate the power radiated by a small circular loop.
            % :param frequency: The operating frequency (Hz)
            % :param radius: The radius of the small circular loop (m).
            % :param current: The current on the small circular loop (A)
            % :return: The radiated power (W)
            
            r = 0.5 * radiation_resistance(obj) * abs(obj.current) ^ 2;
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_field(obj)
            % Calculate the electric and magnetic far fields for a small circular loop.
            % :param r: The range to the field point (m).
            % :param theta: The angle to the field point (rad).
            % :param frequency: The operating frequency (Hz).
            % :param radius: The radius of the small circular loop (m).
            % :param current: The current on the small circular loop (A).
            % :return: The electric and magnetic far fields (V/m) & (A/m).
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Define the radial-component of the electric far field (V/m)
            e_r = 0.0;
            
            % Define the theta-component of the electric far field (V/m)
            e_theta = 0.0;
            
            % Define the phi-component of the electric far field (V/m)
            e_phi = exp(-1j * k * obj.r) * (eta * k * obj.radius * obj.current) / (2.0 * obj.r) .*...
                besselj(1, k * obj.radius * sin(obj.theta));
            
            % Define the r-component of the magnetic far field (A/m)
            h_r = (1j * k * obj.radius^2 * obj.current / (2.0 * obj.r^2) .* ...
                cos(obj.theta)/(1j * k * obj.r) + 1.0) * exp(-1j * k * obj.r);
            
            % Define the theta-component of the magnetic far field (A/m)
            h_theta = -exp(-1j * k * obj.r) * obj.current * k * obj.radius ./ (2.0 * obj.r) .*...
                besselj(1, k * obj.radius .* sin(obj.theta));
            
            % Define the phi-component of the magnetic far field (A/m)
            h_phi = 0.0;
            
        end
        
    end
    
end

