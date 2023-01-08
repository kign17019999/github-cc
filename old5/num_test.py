import ast
def import_config():
    # Open the file in read mode
    with open('config.conf', 'r') as f:
        # Read the lines of the file into a list
        lines = f.readlines()

    # Initialize an empty dictionary to store the parameters
    params = {}

    # Iterate over the lines in the file
    for line in lines:
        # Split the line into a list of words
        words = line.split("=")

        # Extract the parameter name and value from the words
        param_name = words[0]
        param_value = words[1]

        # Strip the quotes from the value, if necessary
        if param_value[0] == "'" or param_value[0] == '"':
            param_value = param_value[1:-1]

        # Convert the value to the appropriate data type
        if param_value == "True":
            param_value = True
        elif param_value == "False":
            param_value = False
        elif param_value.isdigit():
            param_value = int(param_value)
        else:
            try:
                # Use ast.literal_eval to try to parse the value as a list
                param_value = ast.literal_eval(param_value)
            except:
                # If ast.literal_eval raises a ValueError, treat the value as a string
                param_value=param_value[:-1]

        # Add the parameter to the dictionary
        params[param_name] = param_value

    # Print the parameters
    '''
    print(type(params))
    print(params['always_on'])
    print(type(params['always_on']))
    print(params['always_on'][1])
    print(type(params['always_on'][1]))
    print(params['randF'])
    print(params['parallel'])
    print(params['file_name'])
    '''

    for key,value in params.items():
        print(f'{key} : {value}')
    print(type(params['always_on']))
import_config()

aa = {'1':1, '2':2}
print(len(aa))