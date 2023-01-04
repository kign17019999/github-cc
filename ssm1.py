import boto3

# Create an SSM client
ssm = boto3.client('i-089b73b2d2e0c3d6e', region_name = 'us-east-1')

# Execute the command on the instance
response = ssm.send_command(
    InstanceIds=['i-089b73b2d2e0c3d6e'],
    DocumentName='AWS-RunShellScript',
    Comment='Run a script',
    Parameters={'commands': ['cd github-cc', 'nohup python worker3mul.py &']}
)

# Get the command ID
command_id = response['Command']['CommandId']

# Wait for the command to complete
command_completed = False
while not command_completed:
    # Check the status of the command
    command_status = ssm.list_command_invocations(CommandId=command_id)
    command_completed = command_status['Status'] == 'Success'

# Get the command output
command_output = ssm.get_command_invocation(CommandId=command_id, InstanceId='i-089b73b2d2e0c3d6e')
print(command_output['StandardOutputContent'])
