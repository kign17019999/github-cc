import boto3

# Connect to the EC2 service
ec2 = boto3.client('ec2', region_name = 'us-east-1')

# Set the instance ID of the instance you want to start or stop
instance_id = 'i-011e5c83dd72ef526'

# Start the instance
response = ec2.start_instances(InstanceIds=[instance_id])

# Check the status of the start operation
if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print('Instance start successful')
else:
    print('Instance start failed')