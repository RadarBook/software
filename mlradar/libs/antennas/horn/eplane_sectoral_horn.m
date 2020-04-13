classdef eplane_sectoral_horn
    % E-plane sectoral horn antenna
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    %
    % Copyright (C) 2019 Artech House (artech@artechhouse.com)
    % This file is part of Introduction to Radar Using Python and MATLAB
    % and can not be copied and/or distributed without the express permission of Artech House.
    
    properties
        % Properties for E-plane sectoral horn antennas
        guide_width = 0.1; % The width of the waveguide feed (m).
        horn_effective_length = 1.0; % The effective length of the horn (m).
        horn_height = 1.0; % The height of the horn (m).
        frequency = 300.0e6; % The operating frequency (Hz).
        x = 0.0; % The x coordinate to calculate the field in the aperture (m).
        y = 0.0; % The y coordinate to calculate the field in the aperture (m).
        r = 1e9; % The range to the field point (m).
        theta = 0.5 * pi; % The theta angle to the field point (rad).
        phi = 0.5 * pi; % The phi angle to the field point (rad).
    end
    
    methods
        % Methods for E-plane sectoral horn antennas
        function obj = eplane_sectoral_horn(guide_width, horn_height, horn_effective_length, frequency, ...
                x, y, r, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.frequency = frequency;
                obj.guide_width = guide_width;
                obj.horn_height = horn_height;
                obj.horn_effective_length = horn_effective_length;
                obj.x = x;
                obj.y = y;
                obj.r = r;
                obj.theta = theta;
                obj.phi = phi;
            end
        end
        
        
        function [e_x, e_y, e_z, h_x, h_y, h_z] = aperture_fields(obj)
            % Calculate the electric and magnetic fields at the aperture of the horn.
            % Assuming that the fields of the feeding waveguide are those of the dominant TE10 mode.
            % And that the horn length is large compared to the dimensions of the waveguide.
            % :param x: The x coordinate to calculate the field in the aperture (m).
            % :param y: The y coordinate to calculate the field in the aperture (m).
            % :param guide_width: The width of the waveguide feed (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The electric and magnetic fields at the horn aperture (V/m), (A/m).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Define the x-component of the electric field
            e_x = 0.0;
            
            % Define the y-component of the electric field
            e_y = cos(pi * obj.x / obj.guide_width) .* exp(-1j * k * obj.y .^ 2 / (2.0 * obj.horn_effective_length));
            
            % Define the z-component of the electric field
            e_z = 0.0;
            
            % Define the x-component of the magnetic field
            h_x = -cos(pi * obj.x / obj.guide_width) / eta .* exp(-1j * k * obj.y .^ 2 / (2.0 * obj.horn_effective_length));
            
            % Define the y-component of the magnetic field
            h_y = 0.0;
            
            % Define the z-component of the magnetic field
            h_z = 1j * pi / (k * obj.guide_width * eta) * sin(pi * obj.x / obj.guide_width) .* ...
                exp(-1j * k * obj.y .^ 2 / (2.0 * obj.horn_effective_length));
            
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_fields(obj)
            % Calculate the electric and magnetic fields in the far field of the horn.
            % :param r: The distance to the field point (m).
            % :param theta: The theta angle to the field point (rad).
            % :param phi: The phi angle to the field point (rad).
            % :param guide_width: The width of the waveguide feed (m).
            % :param horn_height: The height of the horn (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :param frequency: The operating frequency (Hz).
            % :return: THe electric and magnetic fields radiated by the horn (V/m), (A/m).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Define the radial-component of the electric field
            e_r = 0.0;
            
            % Define the theta-component of the electric field
            e_theta = I(obj) .* sin(obj.phi) .* (1.0 + cos(obj.theta));
            
            % Define the phi-component of the electric field
            e_phi = I(obj) .* cos(obj.phi) .* (1.0 + cos(obj.theta));
            
            % Define the radial-component of the magnetic field
            h_r = 0.0;
            
            % Define the theta-component of the magnetic field
            h_theta = I(obj) .* -cos(obj.phi) / eta .* (1.0 + cos(obj.theta));
            
            % Define the phi-component of the magnetic field
            h_phi = I(obj) .* sin(obj.phi) / eta .* (1.0 + cos(obj.theta));
            
        end
        
        
        function d = directivity(obj)
            % Calculate the directivity for the E-plane sectoral horn.
            % :param guide_width: The width of the waveguide feed (m).
            % :param horn_height: The height of the horn (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The directivity of the E-plane sectoral horn.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Get the Fresnel integrals
            [C, S] = fresnel(obj.horn_height / sqrt(2.0 * obj.horn_effective_length * wavelength));
            
            d = 64.0 * obj.guide_width * obj.horn_effective_length / (pi * wavelength * obj.horn_height) * (C ^ 2 + S ^ 2);
        end
        
        
        function prad = power_radiated(obj)
            % Calculate the normalized power radiated by the E-plane sectoral horn.
            % :param guide_width: The width of the waveguide feed (m).
            % :param horn_height: The height of the horn (m).
            % :return: The power radiated by the E-plane sectoral horn (normalized by |E0|^2) (W).
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the power radiated
            prad = obj.horn_height * obj.guide_width / (4.0 * eta);
        end
        
        
        function a = I(obj)
            % Calculate the integral used in the far field calculations.
            % :param k: The wavenumber (rad/m).
            % :param r: The distance to the field point (m).
            % :param theta: The theta angle to the field point (rad).
            % :param phi: The phi angle to the field point (rad).
            % :param horn_effective_length: The horn effective length (m).
            % :param horn_height: The horn height (m).
            % :param guide_width: The width of the waveguide feed (m).
            % :return: The result of the integral for far field calculations.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the x and y components of the wavenumber
            kx = k .* sin(obj.theta) .* cos(obj.phi);
            ky = k .* sin(obj.theta) .* sin(obj.phi);
            
            % Two separate terms for the Fresnel integrals
            t1 = sqrt(1.0 / (pi * k * obj.horn_effective_length)) .* (-k * obj.horn_height * 0.5 - ky .* obj.horn_effective_length);
            t2 = sqrt(1.0 / (pi * k * obj.horn_effective_length)) .* ( k * obj.horn_height * 0.5 - ky .* obj.horn_effective_length);
            
            [c1, s1] = fresnel(t1);
            [c2, s2] = fresnel(t2);
            
            index = (kx * obj.guide_width ~= pi) & (kx * obj.guide_width ~= -pi);
            term2 = -ones(size(kx)) / pi;
            term2(index) = cos(kx(index) * obj.guide_width * 0.5) ./ ((kx(index) * obj.guide_width * 0.5) .^ 2 - (pi * 0.5) ^ 2);
            
            a = exp(1j * ky .^ 2 * obj.horn_effective_length / (2.0 * k)) * -1j * obj.guide_width * ...
                sqrt(pi * k * obj.horn_effective_length) / (8.0 * obj.r) * exp(-1j * k * obj.r) .* term2 .* ((c2 - c1) - 1j * (s2 - s1));
            
        end
    end
end

