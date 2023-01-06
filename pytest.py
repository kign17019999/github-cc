# Open the file in read mode
with open('dict_file.txt', 'r') as f:
  # Read the contents of the file into a list
  lines = f.readlines()

# Split the lines on the '=' character to get the key-value pairs
pairs = [line.strip().split('=') for line in lines]

# Split the key-value pairs on the ' ' character to get the keys and values
keys_and_values = [pair[1].split(' ') for pair in pairs]

# Zip the keys and values together to create the dictionary
result_dict = {key: value for key, value in keys_and_values}

# Print the resulting dictionary
print(result_dict)
