import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Create a grid of x and y values
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Initial coefficient value
initial_coeff = 1.0

# Calculate initial function z = coeff * y + atan2(x, y)
Z_initial = initial_coeff * Y + np.arctan2(Y, X)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 9))
plt.subplots_adjust(bottom=0.15)  # Make room for the slider

# Create initial contour plot
contourf = ax.contourf(X, Y, Z_initial, levels=20, cmap='RdYlBu', alpha=0.8)
contour = ax.contour(X, Y, Z_initial, levels=20, colors='black', alpha=0.6, linewidths=0.5)

# Add colorbar
cbar = plt.colorbar(contourf, ax=ax, label=f'z = {initial_coeff:.1f} * y + {initial_coeff:.1f}*atan2(y, x)')

# Set labels and formatting
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(f'Contour Plot of z = {initial_coeff:.1f} * y + {initial_coeff:.1f}*atan2(y, x)')
ax.grid(True, alpha=0.3)
ax.axis('equal')

# Create slider axis (left, bottom, width, height)
slider_ax = plt.axes([0.2, 0.07, 0.6, 0.03])
slider = Slider(slider_ax, 'free stream', -3.0, 3.0, valinit=initial_coeff, valfmt='%.2f')
slider2_ax = plt.axes([0.2, 0.01, 0.6, 0.03])
slider2 = Slider(slider2_ax, 'source', -3.0, 3.0, valinit=initial_coeff, valfmt='%.2f')

# Update function
def update(val):
    # Get the current slider value
    coeff = slider.val
    c2 = slider2.val
    
    # Calculate new Z values
    Z_new = coeff * Y + c2/2/3.14*np.arctan2(Y, X)
    
    # Clear the current contour plots
    ax.clear()
    
    # Create new contour plot
    contourf_new = ax.contourf(X, Y, Z_new, levels=20, cmap='RdYlBu', alpha=0.8)
    ax.contour(X, Y, Z_new, levels=20, colors='black', alpha=0.6, linewidths=0.5)
    
    # Update formatting
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Contour Plot of z = {coeff:.2f} * y + {c2:.2f} * atan2(x, y)')
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    
    # Update colorbar
    cbar.mappable.set_array(Z_new)
    cbar.set_label(f'z = {coeff:.2f} * y + {c2:.2f} * atan2(x, y)')
    
    # Redraw
    fig.canvas.draw()

# Connect the slider to the update function
slider.on_changed(update)
slider2.on_changed(update)

# Show the plot
plt.show()