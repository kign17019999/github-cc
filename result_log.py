import csv
import os
import random

def add_or_create_log(fileName, fileDir, dict_data):
# Set the file name and directory
    file_name = fileName
    file_dir = fileDir

    # Check if the file exists in the specified directory
    if not os.path.exists(os.path.join(file_dir, file_name)):
        # Create the file in write mode
        with open(os.path.join(file_dir, file_name), 'w', newline='') as csv_file:
        # Create a CSV writer object
            writer = csv.writer(csv_file)
    
        # Write data to the file
        writer.writerow(dict_data.keys())
        writer.writerow(dict_data.values())
        
        #for key, value in dict_data.items():
        #   writer.writerow(['Name', 'Age'])
    else:
        # Open the file in append mode
        with open(os.path.join(file_dir, file_name), 'a', newline='') as csv_file:
        # Create a CSV writer object
            readers = csv.reader(csv_file)
            headers = next(readers)
            append_dict = {}
            for header in headers:
                append_dict[header] = dict_data[header]
            with open(os.path.join(file_dir, file_name), 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(append_dict.keys())
    return True, fileName, fileDir

if __name__ == '__master__':
    data1 = random.randint(0, 99)
    data2 = random.randint(0, 99)
    status, fileName, fileDir = add_or_create_log(
        fileName = 'test_log.csv',
        fileDir = '/home/ec2-user/github-cc/',
        dict_data = {
            'col1':data1,
            'col2':data2
        }
    )
    if status == True:
        status_print = 'Success saving Log'
    else:
        status_print = 'fail saving Log'
    
    print(f'{status_print} at {fileDir} in {fileName}')
