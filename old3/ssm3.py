import boto3

# Create an SSM client
ssm_client = boto3.client('ssm', region_name = 'us-east-1')

# Specify the ID of the target instance
target_instance_id = 'i-060cca7073b2c2c34'

# Specify the name of the SSM document to use
document_name = 'AWS-RunShellScript'

# Specify the script to run and the working directory
commands = ['python3 h3.py']

workingDirectory = "/home/ec2-user"

# Send the command to the target instance
response = ssm_client.send_command(
    InstanceIds=[target_instance_id],
    DocumentName=document_name,
    Parameters={
        'commands': commands,
        "workingDirectory" : workingDirectory
        },
    Comment='Run1',
    CloudWatchOutputConfig={
        'CloudWatchLogGroupName': '/aws/ssm/{}'.format(document_name),
        'CloudWatchOutputEnabled': True
    }
)

# Print the command ID
print(response['Command']['CommandId'])
