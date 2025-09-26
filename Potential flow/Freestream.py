import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import scipy.ndimage as ndimage

def solve_stream_function(nx, ny, U_inf=1.0):
    """
    Solve for stream function with boundary conditions:
    - Left boundary (inlet): ψ = U_inf * y (free stream)
    - Right boundary (outlet): ψ = U_inf * y (free stream)
    - Top wall: ψ = constant (no flow through wall)
    - Bottom wall: ψ = 0 (no flow through wall)
    """
    # Grid spacing
    dx = 2.0 / (nx - 1)  # Domain from -1 to 1
    dy = 2.0 / (ny - 1)  # Domain from -1 to 1
    
    # Create coordinate arrays
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)
    X, Y = np.meshgrid(x, y)
    
    # Initialize stream function
    psi = np.zeros((ny, nx))
    
    # Set boundary conditions
    # Left boundary (x = -1): free stream ψ = U_inf * y
    psi[:, 0] = U_inf * y
    
    # Right boundary (x = 1): free stream ψ = U_inf * y  
    psi[:, -1] = U_inf * y
    
    # Bottom wall (y = -1): ψ = 0
    psi[0, :] = 0
    
    # Top wall (y = 1): ψ = U_inf * 2 (constant, no flow through)
    psi[-1, :] = U_inf * 2
    
    # Solve Laplace equation ∇²ψ = 0 in the interior using finite differences
    # This is a simplified approach - for more accuracy, use iterative methods
    for iteration in range(5000):  # Simple Gauss-Seidel iteration
        psi_old = psi.copy()
        
        # Interior points: ∇²ψ = 0 discretized as:
        # (ψ[i+1,j] + ψ[i-1,j] - 2ψ[i,j])/dx² + (ψ[i,j+1] + ψ[i,j-1] - 2ψ[i,j])/dy² = 0
        for i in range(1, ny-1):
            for j in range(1, nx-1):
                psi[i, j] = 0.25 * (psi[i+1, j] + psi[i-1, j] + psi[i, j+1] + psi[i, j-1])
        
        # Reapply boundary conditions
        psi[:, 0] = U_inf * y    # Left
        psi[:, -1] = U_inf * y   # Right  
        psi[0, :] = 0            # Bottom
        psi[-1, :] = U_inf * 2   # Top
        
        # Check convergence
        if np.max(np.abs(psi - psi_old)) < 1e-6:
            print(f"Converged after {iteration+1} iterations")
            break
    
    return X, Y, psi

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
nx, ny = 61, 61  # Grid size
U_inf = 1.0      # Free stream velocity

# Solve for stream function
X, Y, psi = solve_stream_function(nx, ny, U_inf)

# Compute grid spacing
dx = 2.0 / (nx - 1)
dy = 2.0 / (ny - 1)

# Compute Laplacian
laplacian_psi = compute_laplacian(psi, dx, dy)

# Create plots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Stream function
contour1 = ax1.contour(X, Y, psi, levels=20, colors='blue', alpha=0.8)
ax1.clabel(contour1, inline=True, fontsize=8)
ax1.set_title('Stream Function ψ')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.grid(True, alpha=0.3)
ax1.axis('equal')
ax1.text(-0.9, 0.8, 'Top Wall\n(ψ = constant)', fontsize=10, bbox=dict(boxstyle="round", facecolor='wheat'))
ax1.text(-0.9, -0.8, 'Bottom Wall\n(ψ = 0)', fontsize=10, bbox=dict(boxstyle="round", facecolor='wheat'))
ax1.text(-0.9, 0, 'Inlet\n(Free stream)', fontsize=10, bbox=dict(boxstyle="round", facecolor='lightblue'))
ax1.text(0.7, 0, 'Outlet\n(Free stream)', fontsize=10, bbox=dict(boxstyle="round", facecolor='lightblue'))

# Plot 2: Laplacian of stream function
contour2 = ax2.contourf(X, Y, laplacian_psi, levels=20, cmap='RdBu_r')
plt.colorbar(contour2, ax=ax2, label='∇²ψ')
contour2_lines = ax2.contour(X, Y, laplacian_psi, levels=20, colors='black', alpha=0.4, linewidths=0.5)
ax2.set_title('Laplacian of Stream Function (∇²ψ)')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.grid(True, alpha=0.3)
ax2.axis('equal')

# Plot 3: Velocity field (from stream function)
# u = ∂ψ/∂y, v = -∂ψ/∂x
u = np.gradient(psi, dy, axis=0)  # ∂ψ/∂y
v = -np.gradient(psi, dx, axis=1)  # -∂ψ/∂x

# Subsample for quiver plot
step = 4
X_sub = X[::step, ::step]
Y_sub = Y[::step, ::step]
u_sub = u[::step, ::step]
v_sub = v[::step, ::step]

ax3.quiver(X_sub, Y_sub, u_sub, v_sub, alpha=0.7)
contour3 = ax3.contour(X, Y, psi, levels=15, colors='blue', alpha=0.5)
ax3.set_title('Velocity Field and Streamlines')
ax3.set_xlabel('x')
ax3.set_ylabel('y')
ax3.grid(True, alpha=0.3)
ax3.axis('equal')

plt.tight_layout()
plt.show()

# Print some statistics
print(f"Stream function range: [{psi.min():.4f}, {psi.max():.4f}]")
print(f"Laplacian range: [{laplacian_psi.min():.6f}, {laplacian_psi.max():.6f}]")
print(f"Max |∇²ψ| (should be close to 0): {np.max(np.abs(laplacian_psi)):.6f}")
