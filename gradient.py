import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib.widgets import Slider

def generate_smooth_gradient_array(rows, cols, min_value, max_value, scale):
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    center_x, center_y = cols // 2, rows // 2
    distance_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    normalized_distance = distance_to_center / np.max(distance_to_center)
    values = min_value + (max_value - min_value) * np.exp(-normalized_distance**2 / scale)
    return values

def update(val):
    slide = slider.val
    if slide < 801:
        scale = 40
    else:
        best_coeff = [-1.70453236e-20,  4.25910350e-17,  -4.69036058e-14,  2.99318966e-11,
                    -1.22371183e-08,  3.34282761e-06, -6.16663475e-04,  7.56768140e-02,
                    -5.89445730e+00,  2.61764360e+02, -4.96488543e+03]
        scale = np.polyval(best_coeff, slide/10)

    smooth_gradient_array = generate_smooth_gradient_array(rows, cols, min_value, max_value, scale)
    
    # Generate x and y coordinates for the meshgrid
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    
    # Generate z coordinates with a range based on the slider value
    z = np.ones_like(x) * slide  # Convert slider value to mm
    
    # Plot the surface with face colors based on smooth_gradient_array
    ax.plot_surface(x, y, z, cmap='viridis', facecolors=plt.cm.viridis(smooth_gradient_array))
    
    # Set labels and limits for axes
    ax.set_xlabel('X (pixels)')
    ax.set_ylabel('Y (pixels)')
    ax.set_zlabel('Scale (mm)')
    ax.set_zlim(0, 4000)  # Limit the z-axis from 0 to 4000 mm based on the slider range
    
    # Print information
    print(f"Calculated slide for scale = {slide}: {scale} mm")
    print(f"Value at (185, 135): {smooth_gradient_array[135, 185]:.2f}")

    # Redraw the plot
    plt.draw()


    return smooth_gradient_array


# Set the size of the array
rows, cols = 480, 270

# Set the range of values
min_value, max_value = 0, 1

# Initial scale value
initial_scale = 1.5

# Calculate the size of the 3D array
size_of_3d_array = rows * cols * 1  # Depth is always 1 in this case

# Print the size of the 3D array
print("Size of the smooth gradient 3D array:", size_of_3d_array)

# Generate the initial smooth gradient array
smooth_gradient_array = generate_smooth_gradient_array(rows, cols, min_value, max_value, initial_scale)

# Create a figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a slider axes and add a slider
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Scale', 0, 4000, valinit=initial_scale)

# Create an empty list to store frames
frames = []

# Iterate over the slider values from 0 to 4000 and update the plot
for slide in range(0, 4001, 10):
    slider.set_val(slide)
    smooth_gradient_array = update(slide)  # Update and get the smooth gradient array
    
    frames.append(smooth_gradient_array[:, :])   # Append the updated array to frames

   

# Convert the list of frames into a numpy array
frames_array = np.array(frames)
frames_array_transposed = np.transpose(frames_array, (1, 2, 0))

np.save('frames_array.npy', frames_array)
print('shape of transposed frame array:', frames_array_transposed.shape)
np.save('frames_array_transposed.npy',frames_array_transposed)

# Display the plot
plt.show()