classdef infinitesimal_dipole
    % Infinitesimal dipole
    % Created by: Lee A. Harrison
    % On: 8/1/2018
    
    properties
        % Infinitesimal dipole properties
        length = 1.0;  % The dipole length (m).
        current = 1.0; % The dipole current (A).
        frequency = 1.0e9; % The operating frequency (Hz).
        r = 1.0e9; % The distance to the field point (m).
        theta = 2.0 * pi; % The angle to the field point (rad).
    end
    
    methods
        % Methods for the infinitesimal dipole
        function obj = infinitesimal_dipole(length, current, frequency, r, theta)
            % Class constructor
            if(nargin > 0)
                obj.length = length;
                obj.current = current;
                obj.frequency = frequency;
                obj.r = r;
                obj.theta = theta;
            end
        end
        
        function d = directivity(obj)
            % The directivity of an infinitesimal dipole antenna.
            % :return: The directivity of an infinitesimal dipole antenna.
            d = 1.5;
        end
        
        function b = beamwidth(obj)
            % The half power beamwidth of an infinitesimal dipole antenna.
            % :return: The half power beamwidth of an infinitesimal dipole antenna (deg).
            b = 90.0;
        end
        
        function ae = maximum_effective_aperture(obj)
            % Calculate the maximum effective aperture of an infinitesimal dipole antenna.
            % :param frequency: The operating frequency (Hz).
            % :return: The maximum effective aperture (m^2).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            ae = 3.0 * wavelength ^ 2 / (8.0 * pi);
        end
        
        
        function r = radiation_resistance(obj)
            % Calculate the radiation resistance for a infinitesimal dipole.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :return: The radiation resistance (Ohms).
            
            % Speed of light
            c = 299792458;
            
            % Calculate and return the radiation resistance
            r = 80.0 * (pi * obj.length * obj.frequency / c) ^ 2;
        end
        
        
        function r = radiated_power(obj)
            % Calculate the power radiated by a infinitesimal dipole.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :param current: The current on the dipole (A).
            % :return: The radiated power (W).
            
            r = 0.5 * radiation_resistance(obj) * abs(obj.current) ^ 2;
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_field(obj)            
            % Calculate the electric and magnetic far fields for a infinitesimal dipole.
            % :param r: The range to the field point (m).
            % :param theta: The angle to the field point (rad).
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :param current: The current on the dipole (A).
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
            e_theta = 1j * eta * k * obj.current * obj.length / (4.0 * pi * obj.r) *...
                sin(obj.theta) * exp(-1j * k * obj.r);
            
            % Define the phi-component of the electric far field (V/m)
            e_phi = 0.0;
            
            % Define the r-component of the magnetic far field (A/m)
            h_r = 0.0;
            
            % Define the theta-component of the magnetic far field (A/m)
            h_theta = 0.0;
            
            % Define the phi-component of the magnetic far field (A/m)
            h_phi = 1j * k * obj.current * obj.length / (4.0 * pi * obj.r) * ...
                sin(obj.theta) * exp(-1j * k * obj.r);
            
            
        end
        
    end
end
