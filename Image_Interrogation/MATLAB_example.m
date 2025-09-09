function MATLAB_example()
    % This function loads an image, displays it, and allows the user to
    % interactively measure the distance between two clicked points.

    path = '/Users/crogers/GitHub/ME51-25/PIV/steady_flow/frame_0_delay-0.14s.png';

    try
        rgbImage = imread(path);
    catch
        error("Error: %s not found. Please provide a valid image file.",path);
    end

    % Convert to grayscale if necessary
    if size(rgbImage, 3) == 3
        grayImage = rgb2gray(rgbImage);
    else
        grayImage = rgbImage; % Already grayscale
    end

    f = figure;
    ax = axes('Parent', f);
    imshow(grayImage, 'Parent', ax);
    title('Click two points on the image to measure distance');

    % Implement interactive functionality 
    % Use a nested function to handle mouse clicks. This is a simple way
    % to manage state between function calls.

    points = [];
    set(f, 'WindowButtonDownFcn', @on_click);
    
    % --- Nested function to handle clicks ---
    function on_click(~, ~)
        % Get the current point from the axes.
        coords = get(ax, 'CurrentPoint');
        x = coords(1, 1);
        y = coords(1, 2);

        % If the click is outside the image axes, do nothing.
        if ~in_axes(ax, x, y)
            return;
        end

        % Store the clicked point.
        points = [points; x, y];
        hold(ax, 'on');
        plot(ax, x, y, 'ro', 'MarkerSize', 5);

        % When two points are selected, calculate and display the distance.
        if size(points, 1) == 2
            x1 = points(1, 1);
            y1 = points(1, 2);
            x2 = points(2, 1);
            y2 = points(2, 2);

            % Calculate the Euclidean distance.
            distance = norm([x2 - x1, y2 - y1]);

            % Display the distance.
            mid_x = (x1 + x2) / 2;
            mid_y = (y1 + y2) / 2;
            text(ax, mid_x, mid_y, sprintf('Distance: %.1f pixels', distance), ...
                'Color', 'red', 'FontSize', 12, 'VerticalAlignment', 'bottom');

            % Draw a line between the two points.
            plot(ax, [x1, x2], [y1, y2], 'r--');
            
            % Clear the points after calculation.
            points = [];
        end
        
        hold(ax, 'off');
    end

    % --- Helper function to check if a click is within the axes limits ---
    function is_valid = in_axes(ax_h, x_coord, y_coord)
        x_lim = get(ax_h, 'XLim');
        y_lim = get(ax_h, 'YLim');
        is_valid = (x_coord >= x_lim(1) && x_coord <= x_lim(2) && ...
                    y_coord >= y_lim(1) && y_coord <= y_lim(2));
    end

end
