function [vertices, faces] = read_facet_model(facet_file)
%% Read a model facet file

% Created by: Lee A. Harrison
% Cretaed on: 1/17/2019

% Open the file
fid = fopen(facet_file, 'r');

% Read the name of the model
model_name = fgetl(fid);

% Read the number of vertices
number_of_vertices = str2num(fgetl(fid));

% Read the vertices
vertices = zeros(number_of_vertices, 3);

for i = 1:number_of_vertices
    line = strtrim(fgetl(fid));
    line_list = strsplit(line, ' ');
    
    % Parse the values
    vertices(i,:) = [str2num(line_list{1}), str2num(line_list{2}), str2num(line_list{3})];
end


% Read the number of faces
number_of_faces = str2num(fgetl(fid));

% Read the faces
faces = zeros(number_of_faces, 3);

for i = 1:number_of_faces
    line = strtrim(fgetl(fid));
    line_list = strsplit(line, ' ');
    
    % Parse the values
    faces(i,:) = [str2num(line_list{1}), str2num(line_list{2}), str2num(line_list{3})];
end

faces = faces + 1;

% Close the file
fclose(fid);

end
