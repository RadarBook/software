function plot_settings(fig)
%% Set default sizes for plotting, so that all plots are consistent.
% :param fig: The current figure
% :return: none
%
% Created by: Lee A. Harrison
% On: 6/19/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Check for an existing figure
if ~exist('fig','var')
    fig = gcf;
end

% Get the current screen size
screen_size = get(0,'ScreenSize');

% Set the height and width of the figure to 80% of the screen size
width  = screen_size(3) * 0.8;
height = screen_size(4) * 0.8;

% Set the left and bottom positions for the figure
left = screen_size(3)/2 - width/2;
bottom = screen_size(4)/2 - height/1.8;

% Set the figure size and position
set(fig, 'Position',[left bottom width height]);

% Set the tick label font size
TickLabelFontSize = 16;

% Set the axis label font size
AxisLabelFontSize = 18;

% Set the title font size
TitleFontSize = 20;

% Set the font weight
FontWeight = 'bold';


% The the list of handles
h_list = get(fig, 'children');

% Loop over each handle
for iHandle = 1:length(h_list)
    
    % If an axis, apply settings
    if(strcmp(get(h_list(iHandle), 'type'), 'axes'))
        
        h_child = get(h_list(iHandle), 'children');
        for iChild = 1:length(h_child)
            if strcmp(get(h_child(iChild), 'type'), 'line')
                set(h_child(iChild), 'linewidth', 2)
            end
        end
        
        set(h_list(iHandle), 'fontweight', FontWeight)
        set(h_list(iHandle), 'fontsize', TickLabelFontSize)
        
        %  title settings
        h = get(h_list(iHandle), 'title');
        set(h, 'fontweight', FontWeight)
        set(h, 'fontsize', TitleFontSize)
        
        %  xlabel settings
        try
            h = get(h_list(iHandle), 'xlabel');
            set(h, 'fontweight', FontWeight)
            set(h, 'fontsize', AxisLabelFontSize)
        catch
        end
        
        %  ylabel settings
        try
            h = get(h_list(iHandle), 'ylabel');
            set(h, 'fontweight', FontWeight)
            set(h, 'fontsize', AxisLabelFontSize)
        catch
        end
        
        %  zlabel settings
        try
            h = get(h_list(iHandle), 'zlabel');
            set(h, 'fontweight', FontWeight)
            set(h, 'fontsize', AxisLabelFontSize)
        catch
        end
    end
end