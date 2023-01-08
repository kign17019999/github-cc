import numpy as np

# Create a NumPy array
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Save the NumPy array to a CSV file
np.savetxt("array.csv", arr, delimiter=",", fmt="%.3f")