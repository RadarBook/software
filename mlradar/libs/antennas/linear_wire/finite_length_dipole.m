classdef finite_length_dipole
    % Finite length dipole
    % Created by: Lee A. Harrison
    % On: 7/10/2018
    %
    % Copyright (C) 2019 Artech House (artech@artechhouse.com)
    % This file is part of Introduction to Radar Using Python and MATLAB
    % and can not be copied and/or distributed without the express permission of Artech House.
    
    properties
        % Finite length dipole porperties
        length = 1.0;  % The dipole length (m).
        current = 1.0; % The dipole current (A).
        frequency = 1.0e9; % The operating frequency (Hz).
        r = 1.0e9; % The distance to the field point (m).
        theta = 2.0 * pi; % The angle to the field point (rad).
    end
    
    methods
        % Methods for the finite length dipole
        function obj = finite_length_dipole(length, current, frequency, r, theta)
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
            % The directivity of a finite length dipole antenna.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :param current: The peak current on the dipole (A).
            % :param r: The range to the field point (m).
            % :param theta: The angle to the field point (rad).
            % :return: The directivity of a small dipole antenna.
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave number times the length
            kl = 2.0 * pi * obj.frequency / c * obj.length;
            
            % Calculate the radiation intensity factor
            factor = eta * abs(obj.current) ^ 2 / (8.0 * pi ^ 2);
            
            % Calculate the power radiated
            power_radiated = radiated_power(obj);
            
            % Calculate the maximum of the radiation intensity
            theta = linspace(eps, 2.0 * pi, 10000);
            u_max = max(((cos(0.5 * kl * cos(theta)) - cos(0.5 * kl)) ./ sin(theta)) .^ 2);
            
            d = 4.0 * pi * factor * u_max / power_radiated;
        end
        
        function b = beamwidth(obj)
            % The half power beamwidth of a finite length dipole antenna.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :return: The half power beamwidth of a small dipole antenna (deg).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber times the length
            kl = 2.0 * pi * obj.frequency / c * obj.length;
            
            % Calculate the normalized radiation intensity
            theta = linspace(eps, 2.0 * pi, 10000);
            f = ((cos(0.5 * kl * cos(theta)) - cos(0.5 * kl)) ./ sin(theta)) .^ 2;
            g = f / max(f);
            
            for iTheta = 1:numel(theta)
                if g(iTheta) >= 0.5
                    theta_half = 0.5 * pi - theta(iTheta);
                    break;
                end
            end
            
            b = 2.0 * theta_half * 180.0 / pi;
        end
        
        function ae = maximum_effective_aperture(obj)
            % Calculate the maximum effective aperture of a finite length dipole antenna.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :param current: The peak current on the dipole (A).
            % :return: The maximum effective aperture (m^2).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            ae = wavelength ^ 2 / (4.0 * pi) * directivity(obj);
        end
        
        function r = radiation_resistance(obj)
            % Calculate the radiation resistance for a finite length dipole.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :return: The radiation resistance (Ohms).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave number times the length
            kl = 2.0 * pi * obj.frequency / c * obj.length;
            
            % Calculate the sin and cos integrals for this frequency and length
            si = sinint(kl);
            ci = cosint(kl);
            
            si2 = sinint(2.0 * kl);
            ci2 = cosint(2.0 * kl);
            
            % Calculate and return the radiation resistance
            r = 60.0 * (0.57721 + log(kl) - ci + 0.5 * sin(kl) * (si2 - 2.0 * si) ...
                + 0.5 * cos(kl) * (0.57721 + log(0.5 * kl) + ci2 - 2.0 * ci));
            
        end
        
        function r = radiated_power(obj)
            % Calculate the power radiated by a finite length dipole.
            % :param frequency: The operating frequency (Hz).
            % :param length: The length of the dipole (m).
            % :param current: The current on the dipole (A).
            % :return: The radiated power (W)
            
            r = 0.5 * radiation_resistance(obj) * abs(obj.current) ^ 2;
        end
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_field(obj)
            % Calculate the electric and magnetic far fields for a finite length dipole.
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
            e_theta = 1j * 0.5 * eta * obj.current / (pi * obj.r) * ...
                (cos(0.5 * k * obj.length * cos(obj.theta)) - cos(0.5 * k * obj.length)) ./...
                sin(obj.theta) * exp(-1j * k * obj.r);
            
            % Define the phi-component of the electric far field (V/m)
            e_phi = 0.0;
            
            % Define the r-component of the magnetic far field (A/m)
            h_r = 0.0;
            
            % Define the theta-component of the magnetic far field (A/m)
            h_theta = 0.0;
            
            % Define the phi-component of the magnetic far field (A/m)
            h_phi = 1j * 0.5 * obj.current / (pi * obj.r) * ...
                (cos(0.5 * k * obj.length * cos(obj.theta)) - cos(0.5 * k * obj.length)) ./...
                sin(obj.theta) * exp(-1j * k * obj.r);
        end
    end
end