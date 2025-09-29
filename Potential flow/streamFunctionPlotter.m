function streamFunctionPlotter()
    % Interactive stream function plotter for source, sink, and free stream
    % Creates a GUI with sliders to control flow parameters
    
    % Create figure and set properties
    fig = figure('Name', 'Stream Function Plotter', 'Position', [100, 100, 1000, 700]);
    
    % Define initial parameters
    params = struct();
    params.source_strength = 2;    % Source strength (m)
    params.sink_strength = -2;     % Sink strength (m)
    params.h = 2;                  % Separation distance
    params.free_stream = 1;        % Free stream velocity (U)
    params.velocity_scale = 0.5;   % Velocity vector scale factor
    
    % Create axes for the plot
    ax = axes('Position', [0.1, 0.3, 0.8, 0.65]);
    
    % Create sliders
    createSliders(fig, params);
    
    % Initial plot
    updatePlot(ax, params);
    
    % Nested function to create sliders
    function createSliders(fig, params)
        % Slider positions [left, bottom, width, height]
        slider_width = 0.3;
        slider_height = 0.03;
        label_height = 0.02;
        
        % Source strength slider
        uicontrol('Style', 'text', 'String', 'Source Strength', ...
            'Position', [50, 150, 120, 20], 'HorizontalAlignment', 'left');
        source_slider = uicontrol('Style', 'slider', 'Min', 0.1, 'Max', 5, ...
            'Value', params.source_strength, 'Position', [50, 130, 200, 20]);
        source_text = uicontrol('Style', 'text', 'String', num2str(params.source_strength), ...
            'Position', [260, 130, 50, 20]);
        
        % Sink strength slider
        uicontrol('Style', 'text', 'String', 'Sink Strength', ...
            'Position', [50, 110, 120, 20], 'HorizontalAlignment', 'left');
        sink_slider = uicontrol('Style', 'slider', 'Min', -5, 'Max', -0.1, ...
            'Value', params.sink_strength, 'Position', [50, 90, 200, 20]);
        sink_text = uicontrol('Style', 'text', 'String', num2str(params.sink_strength), ...
            'Position', [260, 90, 50, 20]);
        
        % Separation distance slider
        uicontrol('Style', 'text', 'String', 'Separation (h)', ...
            'Position', [50, 70, 120, 20], 'HorizontalAlignment', 'left');
        h_slider = uicontrol('Style', 'slider', 'Min', 0.5, 'Max', 5, ...
            'Value', params.h, 'Position', [50, 50, 200, 20]);
        h_text = uicontrol('Style', 'text', 'String', num2str(params.h), ...
            'Position', [260, 50, 50, 20]);
        
        % Free stream velocity slider
        uicontrol('Style', 'text', 'String', 'Free Stream Velocity', ...
            'Position', [50, 30, 120, 20], 'HorizontalAlignment', 'left');
        stream_slider = uicontrol('Style', 'slider', 'Min', 0, 'Max', 3, ...
            'Value', params.free_stream, 'Position', [50, 10, 200, 20]);
        stream_text = uicontrol('Style', 'text', 'String', num2str(params.free_stream), ...
            'Position', [260, 10, 50, 20]);
        
        % Velocity scale slider
        uicontrol('Style', 'text', 'String', 'Velocity Vector Scale', ...
            'Position', [350, 150, 120, 20], 'HorizontalAlignment', 'left');
        scale_slider = uicontrol('Style', 'slider', 'Min', 0.1, 'Max', 2, ...
            'Value', params.velocity_scale, 'Position', [350, 130, 200, 20]);
        scale_text = uicontrol('Style', 'text', 'String', num2str(params.velocity_scale), ...
            'Position', [560, 130, 50, 20]);
        
        % Set slider callbacks
        set(source_slider, 'Callback', @(src, event) sliderCallback(src, source_text, 'source_strength'));
        set(sink_slider, 'Callback', @(src, event) sliderCallback(src, sink_text, 'sink_strength'));
        set(h_slider, 'Callback', @(src, event) sliderCallback(src, h_text, 'h'));
        set(stream_slider, 'Callback', @(src, event) sliderCallback(src, stream_text, 'free_stream'));
        set(scale_slider, 'Callback', @(src, event) sliderCallback(src, scale_text, 'velocity_scale'));
        
        % Slider callback function
        function sliderCallback(slider, text_handle, param_name)
            value = get(slider, 'Value');
            set(text_handle, 'String', sprintf('%.2f', value));
            params.(param_name) = value;
            updatePlot(ax, params);
        end
    end
    
    % Function to calculate and plot stream function
    function updatePlot(ax, params)
        % Define grid
        x_range = [-6, 6];
        y_range = [-4, 4];
        [X, Y] = meshgrid(linspace(x_range(1), x_range(2), 100), ...
                         linspace(y_range(1), y_range(2), 80));
        
        % Source and sink positions
        x_source = -params.h/2;
        x_sink = params.h/2;
        y_source = 0;
        y_sink = 0;
        
        % Calculate distances from source and sink
        r_source = sqrt((X - x_source).^2 + (Y - y_source).^2);
        r_sink = sqrt((X - x_sink).^2 + (Y - y_sink).^2);
        
        % Calculate angles from source and sink
        theta_source = atan2(Y - y_source, X - x_source);
        theta_sink = atan2(Y - y_sink, X - x_sink);
        
        % Stream function components
        % Source contribution: ψ_source = (m/(2π)) * θ
        psi_source = (params.source_strength / (2 * pi)) * theta_source;
        
        % Sink contribution: ψ_sink = (m/(2π)) * θ
        psi_sink = (params.sink_strength / (2 * pi)) * theta_sink;
        
        % Free stream contribution: ψ_free = U * y
        psi_free = params.free_stream * Y;
        
        % Total stream function
        psi_total = psi_source + psi_sink + psi_free;
        
        % Clear and plot
        cla(ax);
        hold(ax, 'on');
        
        % Plot streamlines
        contour(ax, X, Y, psi_total, 20, 'LineWidth', 1.2);
        
        % Calculate velocity components from stream function
        % u = ∂ψ/∂y, v = -∂ψ/∂x
        [psi_x, psi_y] = gradient(psi_total, X(1,2)-X(1,1), Y(2,1)-Y(1,1));
        u_velocity = psi_y;   % u = ∂ψ/∂y
        v_velocity = -psi_x;  % v = -∂ψ/∂x
        
        % Create a coarser grid for velocity vectors to avoid clutter
        skip = 8;  % Show every 8th vector
        X_vec = X(1:skip:end, 1:skip:end);
        Y_vec = Y(1:skip:end, 1:skip:end);
        U_vec = u_velocity(1:skip:end, 1:skip:end);
        V_vec = v_velocity(1:skip:end, 1:skip:end);
        
        % Plot velocity vectors
        quiver(ax, X_vec, Y_vec, U_vec, V_vec, params.velocity_scale, 'k', 'LineWidth', 0.8, 'MaxHeadSize', 0.4);
        
        % Mark source and sink positions
        plot(ax, x_source, y_source, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'red', 'DisplayName', 'Source');
        plot(ax, x_sink, y_sink, 'bs', 'MarkerSize', 10, 'MarkerFaceColor', 'blue', 'DisplayName', 'Sink');
        
        % Add flow direction arrow for free stream
        if params.free_stream > 0
            quiver(ax, -5, 3, 1, 0, 'k', 'LineWidth', 2, 'MaxHeadSize', 0.3);
            text(ax, -4.5, 3.3, 'U', 'FontSize', 12, 'FontWeight', 'bold');
        end
        
        % Set axis properties
        axis(ax, 'equal');
        xlim(ax, x_range);
        ylim(ax, y_range);
        grid(ax, 'on');
        xlabel(ax, 'x');
        ylabel(ax, 'y');
        title(ax, sprintf('Stream Function: Source(%.2f) + Sink(%.2f) + Free Stream(%.2f)', ...
            params.source_strength, params.sink_strength, params.free_stream));
        legend(ax, 'Location', 'northeast');
        colorbar(ax);
        
        hold(ax, 'off');
    end
end

% To run the function, simply call:
% streamFunctionPlotter()