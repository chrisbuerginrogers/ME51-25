import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def solve_stream_function_with_circle(nx, ny, circle_radius=0.2, U_inf=1.0):
    """
    Solve for stream function with a circular obstacle in the center.
    circle_radius: radius of the circular obstacle
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
    
    # Create circular obstacle at center (0, 0)
    circle_center_x, circle_center_y = 0.0, 0.0
    
    # Create mask for circular obstacle
    distance_from_center = np.sqrt((X - circle_center_x)**2 + (Y - circle_center_y)**2)
    circle_mask = distance_from_center <= circle_radius
    
    # Set boundary conditions for domain [-1, 1] x [-1, 1]
    # Left boundary (x = -1): free stream ψ = U_inf * y
    psi[:, 0] = U_inf * y
    
    # Right boundary (x = 1): free stream ψ = U_inf * y  
    psi[:, -1] = U_inf * y
    
    # Bottom wall (y = -1): ψ = -U_inf
    psi[0, :] = -U_inf
    
    # Top wall (y = 1): ψ = +U_inf
    psi[-1, :] = U_inf
    
    # Circular obstacle boundary condition
    # For a circular cylinder, we need ψ = constant on the surface
    # We'll use ψ = 0 on the circle surface (streamline that splits around the circle)
    psi[circle_mask] = 0.0
    
    # Solve Laplace equation ∇²ψ = 0 in the fluid region
    for iteration in range(2000):  # More iterations for convergence with circle
        psi_old = psi.copy()
        
        # Interior points: ∇²ψ = 0
        for i in range(1, ny-1):
            for j in range(1, nx-1):
                if not circle_mask[i, j]:  # Only update fluid points
                    psi[i, j] = 0.25 * (psi[i+1, j] + psi[i-1, j] + psi[i, j+1] + psi[i, j-1])
        
        # Reapply boundary conditions
        psi[:, 0] = U_inf * y    # Left
        psi[:, -1] = U_inf * y   # Right  
        psi[0, :] = -U_inf       # Bottom
        psi[-1, :] = U_inf       # Top
        
        # Circular obstacle - constant stream function
        psi[circle_mask] = 0.0
        
        # Check convergence
        if np.max(np.abs(psi - psi_old)) < 1e-6:
            print(f"Converged after {iteration+1} iterations")
            break
    
    return X, Y, psi, circle_mask

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
nx, ny = 101, 101  # Higher grid resolution for better circle resolution
U_inf = 1.0        # Free stream velocity
initial_radius = 0.2  # Initial circle radius

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
X, Y, psi_initial, circle_mask_initial = solve_stream_function_with_circle(nx, ny, initial_radius, U_inf)

# Compute grid spacing
dx = 2.0 / (nx - 1)
dy = 2.0 / (ny - 1)

# Compute initial Laplacian
laplacian_initial = compute_laplacian(psi_initial, dx, dy)

# Initial plots
def create_plots(psi, laplacian, circle_mask, radius):
    # Clear all axes
    ax1.clear()
    ax2.clear()
    ax3.clear()
    
    # Plot 1: Stream function
    # Mask solid regions
    psi_plot = psi.copy()
    psi_plot[circle_mask] = np.nan
    
    contour1 = ax1.contour(X, Y, psi_plot, levels=25, colors='blue', alpha=0.8)
    ax1.clabel(contour1, inline=True, fontsize=8)
    
    # Draw circle boundary
    circle = plt.Circle((0, 0), radius, fill=True, color='gray', alpha=0.8)
    ax1.add_patch(circle)
    
    ax1.set_title(f'Stream Function ψ (Circle Radius: {radius:.2f})')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    
    # Add flow direction arrows
    ax1.annotate('Flow →', xy=(-0.8, 0.7), fontsize=12, 
                bbox=dict(boxstyle="round", facecolor='lightblue', alpha=0.8))
    
    # Plot 2: Laplacian
    laplacian_plot = laplacian.copy()
    laplacian_plot[circle_mask] = np.nan
    
    # Use symmetric colorbar limits
    vmax = max(abs(laplacian_plot[~np.isnan(laplacian_plot)].min()), 
               abs(laplacian_plot[~np.isnan(laplacian_plot)].max()))
    
    contour2 = ax2.contourf(X, Y, laplacian_plot, levels=20, cmap='RdBu_r', 
                           vmin=-vmax, vmax=vmax)
    cb2 = plt.colorbar(contour2, ax=ax2, label='∇²ψ')
    contour2_lines = ax2.contour(X, Y, laplacian_plot, levels=20, colors='black', 
                                alpha=0.4, linewidths=0.5)
    
    # Draw circle boundary
    circle2 = plt.Circle((0, 0), radius, fill=True, color='gray', alpha=0.8)
    ax2.add_patch(circle2)
    
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
    u[circle_mask] = 0
    v[circle_mask] = 0
    
    # Subsample for quiver plot
    step = 6
    X_sub = X[::step, ::step]
    Y_sub = Y[::step, ::step]
    u_sub = u[::step, ::step]
    v_sub = v[::step, ::step]
    circle_sub = circle_mask[::step, ::step]
    
    # Only plot arrows in fluid regions
    X_fluid = X_sub[~circle_sub]
    Y_fluid = Y_sub[~circle_sub]
    u_fluid = u_sub[~circle_sub]
    v_fluid = v_sub[~circle_sub]
    
    if len(X_fluid) > 0:
        speed = np.sqrt(u_fluid**2 + v_fluid**2)
        ax3.quiver(X_fluid, Y_fluid, u_fluid, v_fluid, speed, 
                  cmap='viridis', alpha=0.8)
    
    # Add streamlines
    contour3 = ax3.contour(X, Y, psi_plot, levels=20, colors='blue', alpha=0.5, linewidths=1)
    
    # Draw circle boundary
    circle3 = plt.Circle((0, 0), radius, fill=True, color='gray', alpha=0.8, edgecolor='black', linewidth=2)
    ax3.add_patch(circle3)
    
    ax3.set_title('Velocity Field and Streamlines')
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.grid(True, alpha=0.3)
    ax3.axis('equal')
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)

# Create initial plots
create_plots(psi_initial, laplacian_initial, circle_mask_initial, initial_radius)

# Create slider
slider = Slider(slider_ax, 'Circle Radius', 0.05, 0.8, valinit=initial_radius, valfmt='%.2f')

# Update function
def update(val):
    radius = slider.val
    
    # Solve with new circle radius
    X_new, Y_new, psi_new, circle_mask_new = solve_stream_function_with_circle(nx, ny, radius, U_inf)
    laplacian_new = compute_laplacian(psi_new, dx, dy)
    
    # Update plots
    create_plots(psi_new, laplacian_new, circle_mask_new, radius)
    
    # Redraw
    fig.canvas.draw()

# Connect slider to update function
slider.on_changed(update)

plt.show()

print("Use the slider to adjust the circular obstacle radius.")
print("Watch how the flow separates and recirculates around the circle.")
print("Larger circles create stronger flow disturbances and higher velocities around the obstacle.")