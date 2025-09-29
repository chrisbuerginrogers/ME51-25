function laplaceStreamSolver()
    % Solves Laplace's equation for stream function in rectangular domain
    % Left inlet: constant velocity U, Right outlet: same velocity U
    % Top and bottom: walls (no-slip boundary conditions)
    
    % Create figure and set properties
    fig = figure('Name', 'Laplace Stream Function Solver', 'Position', [100, 100, 1200, 800]);
    
    % Define initial parameters
    params = struct();
    params.U_inlet = 1.0;          % Inlet velocity
    params.domain_width = 4.0;     % Domain width (L)
    params.domain_height = 2.0;    % Domain height (H)
    params.nx = 81;                % Grid points in x-direction
    params.ny = 41;                % Grid points in y-direction
    params.velocity_scale = 0.8;   % Velocity vector scale factor
    params.max_iterations = 10000;  % Maximum iterations for convergence
    params.tolerance = 1e-6;       % Convergence tolerance
    
    % Create axes for the plot
    ax = axes('Position', [0.1, 0.35, 0.8, 0.6]);
    
    % Create sliders and controls
    createControls(fig, params);
    
    % Initial solution
    updateSolution(ax, params);
    
    % Nested function to create sliders and controls
    function createControls(fig, params)
        % Control positions
        y_start = 220;
        y_spacing = 35;
        
        % Inlet velocity slider
        uicontrol('Style', 'text', 'String', 'Inlet Velocity (U)', ...
            'Position', [50, y_start, 120, 20], 'HorizontalAlignment', 'left');
        U_slider = uicontrol('Style', 'slider', 'Min', 0.2, 'Max', 3.0, ...
            'Value', params.U_inlet, 'Position', [50, y_start-20, 200, 20]);
        U_text = uicontrol('Style', 'text', 'String', sprintf('%.2f', params.U_inlet), ...
            'Position', [260, y_start-20, 50, 20]);
        
        % Domain width slider
        uicontrol('Style', 'text', 'String', 'Domain Width (L)', ...
            'Position', [50, y_start-y_spacing, 120, 20], 'HorizontalAlignment', 'left');
        width_slider = uicontrol('Style', 'slider', 'Min', 2.0, 'Max', 8.0, ...
            'Value', params.domain_width, 'Position', [50, y_start-y_spacing-20, 200, 20]);
        width_text = uicontrol('Style', 'text', 'String', sprintf('%.2f', params.domain_width), ...
            'Position', [260, y_start-y_spacing-20, 50, 20]);
        
        % Domain height slider
        uicontrol('Style', 'text', 'String', 'Domain Height (H)', ...
            'Position', [50, y_start-2*y_spacing, 120, 20], 'HorizontalAlignment', 'left');
        height_slider = uicontrol('Style', 'slider', 'Min', 1.0, 'Max', 4.0, ...
            'Value', params.domain_height, 'Position', [50, y_start-2*y_spacing-20, 200, 20]);
        height_text = uicontrol('Style', 'text', 'String', sprintf('%.2f', params.domain_height), ...
            'Position', [260, y_start-2*y_spacing-20, 50, 20]);
        
        % Grid resolution slider
        uicontrol('Style', 'text', 'String', 'Grid Resolution', ...
            'Position', [50, y_start-3*y_spacing, 120, 20], 'HorizontalAlignment', 'left');
        grid_slider = uicontrol('Style', 'slider', 'Min', 21, 'Max', 101, ...
            'Value', params.nx, 'Position', [50, y_start-3*y_spacing-20, 200, 20]);
        grid_text = uicontrol('Style', 'text', 'String', sprintf('%d', params.nx), ...
            'Position', [260, y_start-3*y_spacing-20, 50, 20]);
        
        % Velocity scale slider
        uicontrol('Style', 'text', 'String', 'Velocity Vector Scale', ...
            'Position', [400, y_start, 150, 20], 'HorizontalAlignment', 'left');
        scale_slider = uicontrol('Style', 'slider', 'Min', 0.1, 'Max', 2.0, ...
            'Value', params.velocity_scale, 'Position', [400, y_start-20, 200, 20]);
        scale_text = uicontrol('Style', 'text', 'String', sprintf('%.2f', params.velocity_scale), ...
            'Position', [610, y_start-20, 50, 20]);
        
        % Solve button
        solve_button = uicontrol('Style', 'pushbutton', 'String', 'Solve', ...
            'Position', [400, y_start-2*y_spacing, 100, 30], 'FontSize', 12, 'FontWeight', 'bold');
        
        % Status text
        status_text = uicontrol('Style', 'text', 'String', 'Ready to solve', ...
            'Position', [520, y_start-2*y_spacing, 200, 30], 'HorizontalAlignment', 'left');
        
        % Set callbacks
        set(U_slider, 'Callback', @(src, event) sliderCallback(src, U_text, 'U_inlet'));
        set(width_slider, 'Callback', @(src, event) sliderCallback(src, width_text, 'domain_width'));
        set(height_slider, 'Callback', @(src, event) sliderCallback(src, height_text, 'domain_height'));
        set(grid_slider, 'Callback', @(src, event) gridCallback(src, grid_text));
        set(scale_slider, 'Callback', @(src, event) sliderCallback(src, scale_text, 'velocity_scale'));
        set(solve_button, 'Callback', @(src, event) solveCallback());
        
        % Slider callback function
        function sliderCallback(slider, text_handle, param_name)
            value = get(slider, 'Value');
            set(text_handle, 'String', sprintf('%.2f', value));
            params.(param_name) = value;
        end
        
        % Grid callback function (integer values)
        function gridCallback(slider, text_handle)
            value = round(get(slider, 'Value'));
            % Ensure odd number for better boundary handling
            if mod(value, 2) == 0
                value = value + 1;
            end
            set(text_handle, 'String', sprintf('%d', value));
            params.nx = value;
            params.ny = round(value * params.domain_height / params.domain_width);
            if mod(params.ny, 2) == 0
                params.ny = params.ny + 1;
            end
        end
        
        % Solve button callback
        function solveCallback()
            set(status_text, 'String', 'Solving...');
            drawnow;
            updateSolution(ax, params);
            set(status_text, 'String', 'Solution complete');
        end
    end
    
    % Function to solve Laplace equation and plot results
    function updateSolution(ax, params)
        % Update grid size based on aspect ratio
        params.ny = round(params.nx * params.domain_height / params.domain_width);
        if mod(params.ny, 2) == 0
            params.ny = params.ny + 1;
        end
        
        % Create computational grid
        x = linspace(0, params.domain_width, params.nx);
        y = linspace(0, params.domain_height, params.ny);
        [X, Y] = meshgrid(x, y);
        
        % Grid spacing
        dx = x(2) - x(1);
        dy = y(2) - y(1);
        
        % Initialize stream function
        psi = zeros(params.ny, params.nx);
        
        % Set boundary conditions
        % Left boundary (inlet): ψ = U * y
        psi(:, 1) = params.U_inlet * y';
        
        % Right boundary (outlet): ψ = U * y (same as inlet for fully developed flow)
        psi(:, end) = params.U_inlet * y';
        
        % Top and bottom walls: constant ψ (no flow through walls)
        psi(1, :) = 0;                              % Bottom wall
        psi(end, :) = params.U_inlet * params.domain_height;  % Top wall
        
        % Solve Laplace equation using iterative method (Gauss-Seidel)
        for iter = 1:params.max_iterations
            psi_old = psi;
            
            % Interior points: ∇²ψ = 0
            % Finite difference: (ψ_{i+1,j} - 2ψ_{i,j} + ψ_{i-1,j})/dx² + (ψ_{i,j+1} - 2ψ_{i,j} + ψ_{i,j-1})/dy² = 0
            for i = 2:params.ny-1
                for j = 2:params.nx-1
                    psi(i, j) = ((psi(i+1, j) + psi(i-1, j)) / dy^2 + ...
                                 (psi(i, j+1) + psi(i, j-1)) / dx^2) / ...
                                (2/dx^2 + 2/dy^2);
                end
            end
            
            % Check convergence
            error = max(max(abs(psi - psi_old)));
            if error < params.tolerance
                fprintf('Converged in %d iterations (error = %.2e)\n', iter, error);
                break;
            end
        end
        
        if iter == params.max_iterations
            fprintf('Maximum iterations reached (error = %.2e)\n', error);
        end
        
        % Calculate velocity components from stream function
        % u = ∂ψ/∂y, v = -∂ψ/∂x
        [psi_x, psi_y] = gradient(psi, dx, dy);
        u_velocity = psi_y;   % u = ∂ψ/∂y
        v_velocity = -psi_x;  % v = -∂ψ/∂x
        
        % Plot results
        cla(ax);
        hold(ax, 'on');
        
        % Plot streamlines
        contour(ax, X, Y, psi, 20, 'LineWidth', 1.2);
        
        % Plot velocity vectors (coarser grid)
        skip_x = max(1, round(params.nx/20));
        skip_y = max(1, round(params.ny/15));
        X_vec = X(1:skip_y:end, 1:skip_x:end);
        Y_vec = Y(1:skip_y:end, 1:skip_x:end);
        U_vec = u_velocity(1:skip_y:end, 1:skip_x:end);
        V_vec = v_velocity(1:skip_y:end, 1:skip_x:end);
        
        quiver(ax, X_vec, Y_vec, U_vec, V_vec, params.velocity_scale, 'k', ...
               'LineWidth', 0.8, 'MaxHeadSize', 0.4);
        
        % Mark boundaries
        plot(ax, [0, 0], [0, params.domain_height], 'r-', 'LineWidth', 3, 'DisplayName', 'Inlet');
        plot(ax, [params.domain_width, params.domain_width], [0, params.domain_height], 'b-', ...
             'LineWidth', 3, 'DisplayName', 'Outlet');
        plot(ax, [0, params.domain_width], [0, 0], 'k-', 'LineWidth', 3, 'DisplayName', 'Wall');
        plot(ax, [0, params.domain_width], [params.domain_height, params.domain_height], ...
             'k-', 'LineWidth', 3, 'DisplayName', 'Wall');
        
        % Add flow direction arrows
        arrow_x = params.domain_width * 0.1;
        quiver(ax, arrow_x, params.domain_height/2, params.U_inlet, 0, 0.5, 'r', ...
               'LineWidth', 3, 'MaxHeadSize', 0.3);
        text(ax, arrow_x, params.domain_height/2 + 0.2, sprintf('U = %.2f', params.U_inlet), ...
             'FontSize', 12, 'FontWeight', 'bold', 'Color', 'red');
        
        % Set axis properties
        axis(ax, 'equal');
        xlim(ax, [0, params.domain_width]);
        ylim(ax, [0, params.domain_height]);
        grid(ax, 'on');
        xlabel(ax, 'x');
        ylabel(ax, 'y');
        title(ax, sprintf('Stream Function Solution (Grid: %dx%d, U=%.2f)', ...
              params.nx, params.ny, params.U_inlet));
        legend(ax, 'Location', 'northeast');
        colorbar(ax);
        
        hold(ax, 'off');
    end
end

% To run the function, simply call:
% laplaceStreamSolver()