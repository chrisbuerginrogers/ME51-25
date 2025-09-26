import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def solve_stream_function_with_step(nx, ny, step_height=0.0, U_inf=1.0):
    """
    Solve for stream function with a step in the bottom wall.
    step_height: height of the step (0 = no step, positive = step up)
    """
    # Grid spacing
    dx = 2.0 / (nx - 1)  # Domain from -1 to 1
    dy = 2.0 / (ny - 1)  # Domain from -1 to 1
    
    # Create coordinate arrays
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, ny)
    X, Y = np.meshgrid(x, y)
    
    # Initialize stream function
    psi = np.zeros((ny, nx))
    
    # Create step geometry - step starts at x = 0
    step_start_idx = nx // 2  # Middle of domain (x = 0)
    
    # Find the indices corresponding to the step height
    step_height_clamped = np.clip(step_height, 0, 1.8)  # Limit step height
    step_idx = int((step_height_clamped + 1) / 2 * (ny - 1))  # Convert height to grid index
    
    # Calculate exit area and velocity for mass conservation
    inlet_area = 2.0  # Full height from -1 to +1
    exit_area = 2.0 - step_height_clamped  # Reduced by step height
    velocity_ratio = inlet_area / exit_area if exit_area > 0 else 1.0
    U_exit = U_inf * velocity_ratio
    
    # Set boundary conditions for domain [-1, 1] x [-1, 1]
    # Left boundary (x = -1): free stream ψ = U_inf * y
    psi[:, 0] = U_inf * y
    
    # Right boundary (x = 1): adjusted for exit velocity and reduced area
    # The stream function must span from the step surface to the top
    y_exit_bottom = -1 + step_height_clamped  # Bottom of exit (top of step)
    y_exit_top = 1  # Top of exit
    
    for i in range(ny):
        if y[i] >= y_exit_bottom:  # Only set values above the step
            # Linear distribution from step surface to top
            psi_exit_bottom = U_inf * y_exit_bottom
            psi_exit_top = U_inf * y_exit_top
            # Scale by velocity ratio to account for area change
            psi[i, -1] = psi_exit_bottom + (psi_exit_top - psi_exit_bottom) * (y[i] - y_exit_bottom) / (y_exit_top - y_exit_bottom) * velocity_ratio
    
    # Bottom wall with step
    # Before step (x < 0): ψ = -U_inf
    psi[0, :step_start_idx] = -U_inf
    # After step (x >= 0): ψ = U_inf * (-1 + step_height) on the step surface
    if step_height > 0:
        psi[step_idx, step_start_idx:] = U_inf * (-1 + step_height)
        # Vertical wall of step
        for i in range(1, step_idx):
            psi[i, step_start_idx] = -U_inf  # Vertical wall condition
    else:
        psi[0, step_start_idx:] = -U_inf
    
    # Top wall (y = 1): ψ = +U_inf
    psi[-1, :] = U_inf
    
    # Create a mask for solid regions (inside the step)
    solid_mask = np.zeros((ny, nx), dtype=bool)
    if step_height > 0:
        for i in range(step_idx + 1):
            solid_mask[i, step_start_idx:] = True
    
    # Solve Laplace equation ∇²ψ = 0 in the fluid region
    for iteration in range(1000):
        psi_old = psi.copy()
        
        # Interior points: ∇²ψ = 0
        for i in range(1, ny-1):
            for j in range(1, nx-1):
                if not solid_mask[i, j]:  # Only update fluid points
                    psi[i, j] = 0.25 * (psi[i+1, j] + psi[i-1, j] + psi[i, j+1] + psi[i, j-1])
        
        # Reapply boundary conditions
        psi[:, 0] = U_inf * y    # Left
        
        # Right boundary with mass conservation
        for i in range(ny):
            if y[i] >= y_exit_bottom:
                psi_exit_bottom = U_inf * y_exit_bottom
                psi_exit_top = U_inf * y_exit_top
                psi[i, -1] = psi_exit_bottom + (psi_exit_top - psi_exit_bottom) * (y[i] - y_exit_bottom) / (y_exit_top - y_exit_bottom) * velocity_ratio
        
        psi[-1, :] = U_inf       # Top
        
        # Bottom wall with step
        psi[0, :step_start_idx] = -U_inf
        if step_height > 0:
            psi[step_idx, step_start_idx:] = U_inf * (-1 + step_height)
            # Vertical wall
            for i in range(1, step_idx):
                psi[i, step_start_idx] = -U_inf
        else:
            psi[0, step_start_idx:] = -U_inf
        
        # Check convergence
        if np.max(np.abs(psi - psi_old)) < 1e-6:
            break
    
    return X, Y, psi, solid_mask

def compute_laplacian(psi, dx, dy):
    """Compute the Laplacian of the stream function using finite differences"""
    ny, nx = psi.shape
    laplacian = np.zeros_like(psi)
    
    # Interior points
    for i in range(1, ny-1):
        for j in range(1, nx-1):
            d2psi_dx2 = (psi[i, j+1] - 2*psi[i, j] + psi[i, j-1]) / dx**2
            d2psi_dy2 = (psi[i+1, j] - 2*psi[i, j] + psi[i-1, j]) / dy**2
            laplacian[i, j] = d2psi_dx2 + d2psi_dy2
    
    return laplacian

# Parameters
nx, ny = 81, 81  # Grid size
U_inf = 1.0      # Free stream velocity
initial_step = 0.0  # Initial step height

# Create the figure and subplots
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 0.05], hspace=0.3, wspace=0.3)

# Create axes for plots
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

# Create axis for slider
slider_ax = fig.add_subplot(gs[1, :])

# Solve initial case
X, Y, psi_initial, solid_mask_initial = solve_stream_function_with_step(nx, ny, initial_step, U_inf)

# Compute grid spacing
dx = 2.0 / (nx - 1)
dy = 2.0 / (ny - 1)

# Compute initial Laplacian
laplacian_initial = compute_laplacian(psi_initial, dx, dy)

# Initial plots
def create_plots(psi, laplacian, solid_mask, step_height):
    # Clear all axes
    ax1.clear()
    ax2.clear()
    ax3.clear()
    
    # Plot 1: Stream function
    # Mask solid regions
    psi_plot = psi.copy()
    psi_plot[solid_mask] = np.nan
    
    contour1 = ax1.contour(X, Y, psi_plot, levels=20, colors='blue', alpha=0.8)
    ax1.clabel(contour1, inline=True, fontsize=8)
    
    # Shade solid regions
    if np.any(solid_mask):
        ax1.contourf(X, Y, solid_mask.astype(float), levels=[0.5, 1.5], colors=['gray'], alpha=0.7)
    
    ax1.set_title(f'Stream Function ψ (Step Height: {step_height:.2f})')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    
    # Plot 2: Laplacian
    laplacian_plot = laplacian.copy()
    laplacian_plot[solid_mask] = np.nan
    
    contour2 = ax2.contourf(X, Y, laplacian_plot, levels=20, cmap='RdBu_r')
    cb2 = plt.colorbar(contour2, ax=ax2, label='∇²ψ')
    contour2_lines = ax2.contour(X, Y, laplacian_plot, levels=20, colors='black', alpha=0.4, linewidths=0.5)
    
    # Shade solid regions
    if np.any(solid_mask):
        ax2.contourf(X, Y, solid_mask.astype(float), levels=[0.5, 1.5], colors=['gray'], alpha=0.7)
    
    ax2.set_title('Laplacian of Stream Function (∇²ψ)')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.grid(True, alpha=0.3)
    ax2.axis('equal')
    ax2.set_xlim(-1, 1)
    ax2.set_ylim(-1, 1)
    
    # Plot 3: Velocity field
    u = np.gradient(psi, dy, axis=0)  # ∂ψ/∂y
    v = -np.gradient(psi, dx, axis=1)  # -∂ψ/∂x
    
    # Mask solid regions for velocity
    u[solid_mask] = 0
    v[solid_mask] = 0
    
    # Subsample for quiver plot
    step = 4
    X_sub = X[::step, ::step]
    Y_sub = Y[::step, ::step]
    u_sub = u[::step, ::step]
    v_sub = v[::step, ::step]
    solid_sub = solid_mask[::step, ::step]
    
    # Only plot arrows in fluid regions
    X_fluid = X_sub[~solid_sub]
    Y_fluid = Y_sub[~solid_sub]
    u_fluid = u_sub[~solid_sub]
    v_fluid = v_sub[~solid_sub]
    
    if len(X_fluid) > 0:
        ax3.quiver(X_fluid, Y_fluid, u_fluid, v_fluid, alpha=0.7)
    
    contour3 = ax3.contour(X, Y, psi_plot, levels=15, colors='blue', alpha=0.5)
    
    # Shade solid regions
    if np.any(solid_mask):
        ax3.contourf(X, Y, solid_mask.astype(float), levels=[0.5, 1.5], colors=['gray'], alpha=0.7)
    
    ax3.set_title('Velocity Field and Streamlines')
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.grid(True, alpha=0.3)
    ax3.axis('equal')
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)

# Create initial plots
create_plots(psi_initial, laplacian_initial, solid_mask_initial, initial_step)

# Create slider
slider = Slider(slider_ax, 'Step Height', 0.0, 1.5, valinit=initial_step, valfmt='%.2f')

# Update function
def update(val):
    step_height = slider.val
    
    # Solve with new step height
    X_new, Y_new, psi_new, solid_mask_new = solve_stream_function_with_step(nx, ny, step_height, U_inf)
    laplacian_new = compute_laplacian(psi_new, dx, dy)
    
    # Update plots
    create_plots(psi_new, laplacian_new, solid_mask_new, step_height)
    
    # Redraw
    fig.canvas.draw()

# Connect slider to update function
slider.on_changed(update)

plt.show()

print("Use the slider to adjust the step height in the bottom wall.")
print("Step starts at x = 0 and extends to the outlet.")
print("Exit velocity increases with step height to conserve mass flow.")