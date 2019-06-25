classdef small_loop
    % Small loop antenna
    % Created by: Lee A. Harrison
    % On: 8/1/2018
    
    properties
        % Small loop antenna properties
        radius = 1.0;  % The loop radius (m).
        current = 1.0; % The dipole current (A).
        frequency = 1.0e9; % The operating frequency (Hz).
        r = 1.0e9; % The distance to the field point (m).
        theta = 2.0 * pi; % The angle to the field point (rad).
    end
    
    methods
        % Methods for small loop antenna
        function obj = small_loop(radius, current, frequency, r, theta)
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
            % The directivity of a small loop antenna.
            % :return: The directivity.
            
            d = 1.5;
        end
        
        
        function b = beamwidth(obj)
            % The half power beamwidth of a small loop antenna.
            % :return: The beamwidth (deg).
            
            b = 90.0;
        end
        
        
        function ae = maximum_effective_aperture(obj)
            % Calculate the maximum effective aperture of an small loop antenna.
            % :param frequency: The operating frequency (Hz).
            % :return: The maximum effective aperture (m^2).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            ae = 3.0 * wavelength ^ 2 / (8.0 * pi);
        end
        
        
        function r = radiation_resistance(obj)
            % Calculate the radiation resistance for a small circular loop.
            % :param frequency: The operating frequency (Hz).
            % :param radius: The radius of the small circular loop (m).
            % :return: The radiation resistance (Ohms).
            
            % Speed of light
            c = 299792458;
            
            % Calculate and return the radiation resistance
            r = 20.0 * pi^2 * (2.0 * pi * obj.radius * obj.frequency / c) ^ 4;
        end
        
        
        function r = radiated_power(obj)
            % Calculate the power radiated by a small circular loop.
            % :param frequency: The operating frequency (Hz).
            % :param radius: The radius of the small circular loop (m).
            % :param current: The current on the small circular loop (A).
            % :return: The radiated power (W).
            
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
            e_phi =  (eta * (k * obj.radius)^2 * obj.current / (4.0 * obj.r) * ...
                sin(obj.theta) / (1j * k * obj.r) + 1.0) * exp(-1j * k * obj.r);
            
            % Define the r-component of the magnetic far field (A/m)
            h_r = (1j * k * obj.radius^2 * obj.current / (2.0 * obj.r^2) * ...
                cos(obj.theta)/(1j * k * obj.r) + 1.0) * exp(-1j * k * obj.r);
            
            % Define the theta-component of the magnetic far field (A/m)
            h_theta = -(k * obj.radius)^2 * obj.current / (4.0 * obj.r) * ...
                sin(obj.theta) * (1./(1j * k * obj.r) + (1.0 - 1.0 / (k * obj.r)^2))...
                * exp(-1j * k * obj.r);
            
            % Define the phi-component of the magnetic far field (A/m)
            h_phi = 0.0;
            
        end
        
    end
    
end
