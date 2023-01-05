import boto3

# Connect to the EC2 service
ec2 = boto3.client('ec2', region_name = 'us-east-1')

# Use the describe_instances method to retrieve a list of all instances
response = ec2.describe_instances()

# Iterate through the list of instances and print out the desired information
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        # Get the instance name from the tag (if it exists)
        instance_name = 'N/A'
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                instance_name = tag['Value']
                break
        # Print out the instance information
        print(f'Instance name: {instance_name}, Instance ID: {instance["InstanceId"]}, Running status: {instance["State"]["Name"]}')
