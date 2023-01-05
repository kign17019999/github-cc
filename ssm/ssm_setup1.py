import boto3

# Create an SSM client
ssm_client = boto3.client('ssm', region_name = 'us-east-1')

# Specify the ID of the target instance
# 06
target_instance_id = 'i-011e5c83dd72ef526'

# Specify the name of the SSM document to use
document_name = 'AWS-RunShellScript'

# Specify the script to run and the working directory
commands = ['cd /home/ec2-user && sudo yum install vim git -y && sudo pip3 install numpy && sudo pip3 install boto3 && git clone https://github.com/kign17019999/github-cc.git && cd /home/ec2-user/github-cc']

# Send the command to the target instance
response = ssm_client.send_command(
    InstanceIds=[target_instance_id],
    DocumentName=document_name,
    Parameters={'commands': commands},
    Comment='StartRunR2',
    CloudWatchOutputConfig={
        'CloudWatchLogGroupName': '/aws/ssm/{}'.format(document_name),
        'CloudWatchOutputEnabled': True
    }
)

# Print the command ID
print(response['Command']['CommandId'])
