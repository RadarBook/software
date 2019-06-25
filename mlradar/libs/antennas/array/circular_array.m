classdef circular_array
    % Circular arrays
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    
    properties
        % Properties for circular arrays
        number_of_elements = 21; % The number of elements in the array.
        radius = 1.0; % The radius of the circular array (m).
        frequency = 300.0e6; % The operating frequency (Hz).
        scan_angle_theta = 0.5 * pi; % The theta scan angle of the main lobe (rad).
        scan_angle_phi = 0.5 * pi; % The phi scan angle of the main lobe (rad).
        theta = 0.5 * pi; % The theta angle at which to evaluate the array factor (rad).
        phi = 0.5 * pi; % The phi angle at which to evaluate the array factor (rad).
    end
    
    methods
        % Methods for circular arrays
        function obj = circular_array(number_of_elements, radius, frequency, scan_angle_theta, ...
                scan_angle_phi, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.frequency = frequency;
                obj.number_of_elements = number_of_elements;
                obj.scan_angle_theta = scan_angle_theta;
                obj.scan_angle_phi = scan_angle_phi;
                obj.theta = theta;
                obj.phi = phi;
                obj.radius = radius;
            end
        end
        
        
        function af = array_factor(obj)
            % Calculate the array factor for a circular uniform array.
            % :param number_of_elements: The number of elements in the array.
            % :param radius: The radius of the circular loop (m).
            % :param frequency: The operating frequency (Hz).
            % :param scan_angle_theta: The theta scan angle of the main beam (rad).
            % :param scan_angle_phi: The phi scan angle of the main beam (rad).
            % :param theta: The theta pattern angle (rad).
            % :param phi: The phi pattern angle (rad).
            % :return: The array factor of a circular uniform array.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the angular position of each element
            phi_el = 2.0 * pi / obj.number_of_elements * (0:obj.number_of_elements-1);
            
            % Calculate the phase term
            af = zeros(size(obj.theta));
            for iPhi = 1:numel(phi_el)
                af = af + exp(1j * (k * obj.radius) * (sin(obj.theta) .* cos(obj.phi - phi_el(iPhi)) - ...
                    sin(obj.scan_angle_theta) * cos(obj.scan_angle_phi - phi_el(iPhi))));
            end
            % Return the normalized array factor
            af = af ./ max(max(abs(af)));
        end
    end
end

