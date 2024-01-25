import matplotlib.pyplot as plt
import numpy as np

# Example matrix of RGB values
rgb_matrix = np.random.random((5, 5, 3))  # Shape (5, 5, 3) for RGB colors

# Display the image
plt.imshow(rgb_matrix)

# Show the plot
plt.show()
print(rgb_matrix)