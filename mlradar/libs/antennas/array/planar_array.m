classdef planar_array
    % Planar arrays
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    
    properties
        % Properties of planar arrays
        number_of_elements_x = 21; % The number of array elements in the x direction.
        number_of_elements_y = 21; % The number of array elements in the y direction.
        element_spacing_x = 0.5; % The spacing between each element in the x direction (m).
        element_spacing_y = 0.25; % The spacing between each element in the y direction (m).
        frequency = 300.0e6; % The operating frequency (Hz).
        scan_angle_theta = 0.5 * pi; % The theta scan angle of the main lobe (rad).
        scan_angle_phi = 0.5 * pi; % The phi scan angle of the main lobe (rad).
        theta = 0.5 * pi; % The theta angle at which to evaluate the array factor (rad).
        phi = 0.5 * pi; % The phi angle at which to evaluate the array factor (rad).
    end
    
    methods
        % Methods associated with planar arrays
        function obj = planar_array(number_of_elements_x, number_of_elements_y, element_spacing_x, element_spacing_y, ...
                frequency, scan_angle_theta, scan_angle_phi, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.frequency = frequency;
                obj.number_of_elements_x = number_of_elements_x;
                obj.number_of_elements_y = number_of_elements_y;
                obj.element_spacing_x = element_spacing_x;
                obj.element_spacing_y = element_spacing_y;
                obj.scan_angle_theta = scan_angle_theta;
                obj.scan_angle_phi = scan_angle_phi;
                obj.theta = theta;
                obj.phi = phi;
            end
        end
        
        function [af, psi_x, psi_y] = array_factor(obj)
            % Calculate the array factor for a planar uniform array.
            % :param number_of_elements_x: The number of elements in the x-direction.
            % :param number_of_elements_y: The number of elements in the y-direction.
            % :param element_spacing_x: The spacing of the elements in the x-direction (m).
            % :param element_spacing_y: The spacing of the elements in the y-direction (m).
            % :param frequency: The operating frequency (Hz).
            % :param scan_angle_theta: The scan angle in the theta-direction (rad).
            % :param scan_angle_phi: The scan angle in the phi-direction (rad).
            % :param theta: The pattern angle in theta (rad).
            % :param phi: The pattern angle in phi (rad).
            % :return: The array factor for a planar uniform array.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave number
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the phase
            psi_x = k * obj.element_spacing_x * (sin(obj.theta) .* cos(obj.phi) - sin(obj.scan_angle_theta) * cos(obj.scan_angle_phi));
            psi_y = k * obj.element_spacing_y * (sin(obj.theta) .* sin(obj.phi) - sin(obj.scan_angle_theta) * sin(obj.scan_angle_phi));
            
            % Break into numerator and denominator
            numerator = sin(0.5 * obj.number_of_elements_x * psi_x) .* sin(0.5 * obj.number_of_elements_y * psi_y);
            denominator = obj.number_of_elements_x * obj.number_of_elements_y * sin(0.5 * psi_x) .* sin(0.5 * psi_y);
            
            af = ones(size(psi_x));
            
            index = denominator ~= 0.0;
            
            af(index) = numerator(index) ./ denominator(index);
            
        end
    end
end