classdef pyramidal_horn
    % Pyramidal horn antenna
    % Created by: Lee A. Harrison
    % On:  8/2/2018
    %
    % Copyright (C) 2019 Artech House (artech@artechhouse.com)
    % This file is part of Introduction to Radar Using Python and MATLAB
    % and can not be copied and/or distributed without the express permission of Artech House.
    
    properties
        % Properties associated with pyramidal horn antennas
        horn_width = 1.0; % The horn width (m).
        horn_height = 1.0; % The horn height (m).
        eplane_effective_length = 1.0; % The effective length in the E plane (m).
        hplane_effective_length = 1.0; % The effective length in the H plane (m).
        frequency = 300.0e6; % The operating frequency (Hz).
        x = 0.0; % The x coordinate to calculate the field in the aperture (m).
        y = 0.0; % The y coordinate to calculate the field in the aperture (m).
        r = 1.0e6; % The range to the field point (m).
        theta = 0.5 * pi; % The theta angle to the field point (rad).
        phi = 0.5 * pi; % The phi angle to the field point (rad).
    end
    
    methods
        % Methods associated with pyramidal horn antennas
        function obj = pyramidal_horn(horn_width, horn_height, eplane_effective_length, hplane_effective_length, ...
                frequency, x, y, r, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.frequency = frequency;
                obj.horn_width = horn_width;
                obj.horn_height = horn_height;
                obj.eplane_effective_length = eplane_effective_length;
                obj.hplane_effective_length = hplane_effective_length;
                obj.x = x;
                obj.y = y;
                obj.r = r;
                obj.theta = theta;
                obj.phi = phi;
            end
        end
        
        function [e_x, e_y, e_z, h_x, h_y, h_z] = aperture_fields(obj)
            %     Calculate the electric field at the aperture of the horn.
            %     Assuming that the fields of the feeding waveguide are those of the dominant TE10 mode.
            %     And that the horn length is large compare to the dimensions of the waveguide.
            %     :param x: The x coordinate to calculate the field in the aperture (m).
            %     :param y: The y coordinate to calculate the field in the aperture (m).
            %     :param horn_width: The width of the horn (m).
            %     :param eplane_effective_length: The horn effective length in the E-plane (m).
            %     :param hplane_effective_length: The horn effective length in the H-plane (m).
            %     :param frequency: The operating frequency (Hz).
            %     :return: The electric and magnetic fields at the horn aperture (V/m), (A/m).
            
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Define the x-component of the electric field
            e_x = 0.0;
            
            % Define the y-component of the electric field
            e_y = cos(pi * obj.x / obj.horn_width) .* exp(-1j * k * 0.5 * (obj.x .^ 2 / obj.hplane_effective_length +...
                obj.y .^ 2 / obj.eplane_effective_length));
            
            % Define the z-component of the electric field
            e_z = 0.0;
            
            % Define the x-component of the magnetic field
            h_x = -cos(pi * obj.x / obj.horn_width) / eta .* exp(-1j * k * 0.5 * (obj.x .^ 2 / obj.hplane_effective_length +...
                obj.y .^ 2 / obj.eplane_effective_length));
            
            % Define the y-component of the magnetic field
            h_y = 0.0;
            
            % Define the z-component of the magnetic field
            h_z = 0.0;
            
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_fields(obj)
            %             Calculate the electric and magnetic fields in the far field of the horn.
            %             :param r: The distance to the field point (m).
            %             :param theta: The theta angle to the field point (rad).
            %             :param phi: The phi angle to the field point (rad).
            %             :param horn_width: The width of the horn (m).
            %             :param horn_height: The height of the horn (m).
            %             :param eplane_effective_length: The horn effective length in the E-plane (m).
            %             :param hplane_effective_length: The horn effective length in the H-plane (m).
            %             :param frequency: The operating frequency (Hz).
            %             :return: THe electric and magnetic fields radiated by the horn (V/m), (A/m).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Define the radial-component of the electric field
            e_r = 0.0;
            
            % Define the theta-component of the electric field
            e_theta = 1j * k / (4.0 * pi * obj.r) * exp(-1j * k * obj.r) * sin(obj.phi) .* (1.0 + cos(obj.theta)) .* I1(obj) .* I2(obj);
            
            % Define the phi-component of the electric field
            e_phi = 1j * k / (4.0 * pi * obj.r) * exp(-1j * k * obj.r) * cos(obj.phi) .* (1.0 + cos(obj.theta)) .* I1(obj) .* I2(obj);
            
            % Define the radial-component of the magnetic field
            h_r = 0.0;
            
            % Define the theta-component of the magnetic field
            h_theta = 1j * k / (4.0 * pi * obj.r) * exp(-1j * k * obj.r) * -cos(obj.phi) .* (1.0 + cos(obj.theta)) / eta .* I1(obj) .* I2(obj);
            
            % Define the phi-component of the magnetic field
            h_phi = 1j * k / (4.0 * pi * obj.r) * exp(-1j * k * obj.r) * sin(obj.phi) .* (1.0 + cos(obj.theta)) / eta .* I1(obj) .* I2(obj);
            
        end
        
        
        function d = directivity(obj)
            %             Calculate the directivity for a pyramidal horn.
            %             :param horn_width: The width of the horn (m).
            %             :param horn_height: The height of the horn (m).
            %             :param eplane_effective_length: The horn effective length in the E-plane (m).
            %             :param hplane_effective_length: The horn effective length in the H-plane (m).
            %             :param frequency: The operating frequency (Hz).
            %             :return: The directivity of the pyramidal horn.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the arguments for the Fresnel integrals
            u = 1.0 / sqrt(2.0) * (sqrt(wavelength * obj.hplane_effective_length) / obj.horn_width + obj.horn_width / sqrt(wavelength * obj.hplane_effective_length));
            v = 1.0 / sqrt(2.0) * (sqrt(wavelength * obj.hplane_effective_length) / obj.horn_width - obj.horn_width / sqrt(wavelength * obj.hplane_effective_length));

            % Calculate the Fresnel sin and cos integrals
            [Cu, Su] = fresnel(u);
            [Cv, Sv] = fresnel(v);
            
            arg = obj.horn_height / sqrt(2.0 * wavelength * obj.eplane_effective_length);
            
            [C2, S2] = fresnel(arg);
            C2 = C2 * C2;
            S2 = S2 * S2;
            
            d = 8.0 * pi * obj.eplane_effective_length * obj.hplane_effective_length / (obj.horn_width * obj.horn_height) * ((Cu - Cv) .^ 2 + (Su - Sv) .^ 2) * (C2 + S2);
        end
        
        
        function prad = power_radiated(obj)
            %         Calculate the normalized power radiated by the pyramidal horn.
            %         :param horn_width: The width of the horn (m).
            %         :param horn_height: The height of the horn (m).
            %         :return: The power radiated by the pyramidal horn (normalized by |E0|^2) (W).
            
            % Calculate the normalized power radiated
            prad = obj.horn_width * obj.horn_height / (4.0 * 120.0 * pi);
        end
        
        
        function a = I1(obj)
            %         Calculate the integral used for far field calculations.
            %             :param k: The wavenumber (rad/m).
            %             :param horn_width: The width of the horn (m).
            %             :param hplane_effective_length: The horn effective length in the H-plane (m).
            %             :param theta: The theta angle to the field point (rad).
            %             :param phi: The phi angle to the field point (rad).
            %             :return: The integral used for far field calculations.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the x-component of the wavenumber primed
            kx_p = k * sin(obj.theta) .* cos(obj.phi) + pi / obj.horn_width;
            kx_m = k * sin(obj.theta) .* cos(obj.phi) - pi / obj.horn_width;
            
            % Calculate the arguments of the Fresnel integrals
            t1_p = sqrt(1.0 / (pi * k * obj.hplane_effective_length)) .* (-k * obj.horn_width / 2.0 - kx_p .* obj.hplane_effective_length);
            t2_p = sqrt(1.0 / (pi * k * obj.hplane_effective_length)) .* ( k * obj.horn_width / 2.0 - kx_p .* obj.hplane_effective_length);
            
            t1_m = sqrt(1.0 / (pi * k * obj.hplane_effective_length)) .* (-k * obj.horn_width / 2.0 - kx_m .* obj.hplane_effective_length);
            t2_m = sqrt(1.0 / (pi * k * obj.hplane_effective_length)) .* ( k * obj.horn_width / 2.0 - kx_m .* obj.hplane_effective_length);
            
            % Calculate the Fresnel integrals
            [c1p, s1p] = fresnel(t1_p);
            [c2p, s2p] = fresnel(t2_p);
            
            [c1m, s1m] = fresnel(t1_m);
            [c2m, s2m] = fresnel(t2_m);
            
            % Build the terms from the Fresnel integrals
            fresnel_term1 = (c2p - c1p) + 1j * (s1p - s2p);
            fresnel_term2 = (c2m - c1m) + 1j * (s1m - s2m);
            
            % Calculate the phase terms
            phase_term1 = exp(1j * kx_p .^ 2 * obj.hplane_effective_length / (2.0 * k));
            phase_term2 = exp(1j * kx_m .^ 2 * obj.hplane_effective_length / (2.0 * k));
            
            a = 0.5 * sqrt(pi * obj.hplane_effective_length / k) .* (phase_term1 .* fresnel_term1 + phase_term2 .* fresnel_term2);
        end
        
        function a = I2(obj)
            %             Calculate the integral used for far field calculations.
            %             :param k: The wavenumber (rad/m).
            %             :param horn_height: The height of the horn (m).
            %             :param eplane_effective_length: The horn effective length in the E-plane (m).
            %             :param theta: The theta angle to the field point (rad).
            %             :param phi: The phi angle to the field point (rad).
            %             :return: The integral used for far field calculations.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the y-component of the wavenumber
            ky = k * sin(obj.theta) .* sin(obj.phi);
            
            % Calculate the arguments for the Fresnel integrals
            t1 = sqrt(1.0 / (pi * k * obj.eplane_effective_length)) .* (-k * obj.horn_height / 2.0 - ky .* obj.eplane_effective_length);
            t2 = sqrt(1.0 / (pi * k * obj.eplane_effective_length)) .* ( k * obj.horn_height / 2.0 - ky .* obj.eplane_effective_length);
            
            % Calculate the Fresnel integrals
            [c1, s1] = fresnel(t1);
            [c2, s2] = fresnel(t2);
            
            a = sqrt(pi * obj.eplane_effective_length / k) .* exp(1j * ky .^ 2 * obj.eplane_effective_length / (2.0 * k)) .* ((c2 - c1) + 1j .* (s1 - s2));
            
        end
        
    end
    
end

