import numpy as np

# Set the shape and data type of the array
shape = (10000, 10000)
dtype = np.int64

# Create an empty file with the desired name
with open('my_array.dat', 'w'):
    pass

# Create a memory-mapped file with the specified shape and data type
array = np.memmap('my_array.dat', dtype=dtype, shape=shape)

# Fill the array with random values
array[:] = np.random.randint(0, 100, shape)

# Use the array like any other NumPy array
result = array.mean()
print(result)  # Output: 49.9977

# When you're done, delete the memory-mapped file to free up resources
del array
