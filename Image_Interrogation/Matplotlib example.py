import matplotlib.pyplot as plt

path = '/Users/crogers/GitHub/ME51-25/PIV/steady_flow/frame_0_delay-0.14s.png'
try:
    data = plt.imread(path)
except FileNotFoundError:
    print(f"Error: {path} not found. Please provide a valid image file.")
    exit()
    
# set up plot (plot and color bar
fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis')
fig.colorbar(im, ax=ax, label='Data Value')
ax.set_title("Click two points to measure distance")


points = []

def on_click(event):
    """
    if the user clicks, then either grab the point coordinates and draw a dot
    or if it is the second point, draw the line and show the distance
    """
    # Check if the click was inside the plot area and not on the toolbar
    if event.inaxes != ax:
        return

    x, y = int(round(event.xdata)), int(round(event.ydata))

    points.append((x, y))
    ax.plot(x, y, 'ro', markersize=5)  # Mark the clicked point - red, symbol size 5

    # When two points are selected
    if len(points) == 2:
        x1, y1 = points[0]
        x2, y2 = points[1]

        distance = ((x2-x1)**2 + (y2-y1)**2)**0.5

        # Update the text with the calculated distance
        dist_text = ax.text(0, 0, '', color='white', fontsize=12, va='top')
        dist_text.set_text(f'd={distance:.1f}') #one number past the decimal point
        dist_text.set_position(((x1 + x2) / 2, (y1 + y2) / 2))

        # Draw a line between the two points
        ax.plot([x1, x2], [y1, y2], 'r--')  # red line dotted
        
        # Clear the points after calculation
        points.clear()
        
    # Draw the canvas
    fig.canvas.draw_idle()

# Connect the click event to the handler function
connection_id = fig.canvas.mpl_connect('button_press_event', on_click)

# show plot
plt.show()
