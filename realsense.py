import pyrealsense2 as rs
import numpy as np
import cv2

# Configure pipeline to stream depth frames
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 480, 270, rs.format.z16, 30)

# Start streaming with configured settings
pipeline.start(config)

# Load the frames_array_transposed.npy file
frames_array_transposed = np.load('frames_array_transposed.npy')
# print("Shape of frames_array_transposed:", frames_array_transposed.shape)

# Initialize an empty list to store division results
val_values = []

try:
    while True:
        # Wait for the next set of frames
        frames = pipeline.wait_for_frames()
        
        # Get depth frame
        depth_frame = frames.get_depth_frame()
        
        if not depth_frame:
            continue

        # Convert depth frame to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap for visualization (optional)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Display the depth frame
        cv2.imshow('Depth Frame', depth_colormap)
        
        # Iterate through each pixel to print depth values and values at coordinates
        for y in range(270):
            for x in range(480):
                if x % 10 == 0 and y % 10 == 0:
                    # Print depth value at current coordinates
                    depth_value = depth_image[y, x]

                    if depth_value > 4000:
                        depth_value = 4000
                    # print("Depth value at coordinates ({}, {}):".format(x, y), depth_value)
                
                    # Calculate the new z-coordinate based on depth value
                    z_new = depth_value // 10
               
                    value_at_coordinates = frames_array_transposed[x, y, int(z_new)]
                    # print("Value at coordinates ({}, {}, {}):".format(x, y, int(z_new)), value_at_coordinates)
                    
                    # Calculate the division result
                    val = int(z_new / value_at_coordinates)
                    # print("the division gives val:", val)
                    # Append the division result to the list
                    val_values.append(val)
                    # Convert the list of division results to a NumPy array
                    val_values_array = np.array(val_values)
                    # print("Shape of val array:", val_values_array.shape)
        
        # Check for key press to exit the loop
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
   
    
    # Find the minimum non-zero value in the array
        min_non_zero_value = np.min(val_values_array[np.nonzero(val_values_array)])
        print("Minimum non-zero value:", min_non_zero_value)
        val_value_array= []
        val_values= []
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
