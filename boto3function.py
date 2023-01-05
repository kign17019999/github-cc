import boto3

class Boto3Function():
    def __init__(self, region_name):
        self.ec2 = boto3.client('ec2', region_name = region_name)
        self.sqs = boto3.client('sqs', region_name = region_name)
        self.ssm_client = boto3.client('ssm', region_name = region_name)


    def ec2_status(self):
        # Use the describe_instances method to retrieve a list of all instances
        response = self.ec2.describe_instances()

        inst_dict = {}

        # Iterate through the list of instances and print out the desired information
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                # Get the instance name from the tag (if it exists)
                instance_name = 'N/A'
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        inst_dict[instance_name] = [instance["InstanceId"],instance["State"]["Name"]]
                        break
        return inst_dict

    def ec2_start(self, instance_id):
        response = self.ec2.start_instances(InstanceIds=[instance_id])
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            start = True
        else:
            start = False

        return start

    def ec2_stop(self, instance_id):
        response = self.ec2.stop_instances(InstanceIds=[instance_id])
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            stop = True
        else:
            stop = False

        return stop
    
    def sqs_check_queue(self, queue_url):
        # Use the get_queue_attributes method to retrieve the number of messages in the queue
        response = self.sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )

        # Get the number of messages from the response
        num_messages = int(response['Attributes']['ApproximateNumberOfMessages'])
        
        # get queue name
        queue_name = queue_url.rsplit('/', 1)[-1]

        return queue_name, num_messages

        
    def execute_ssm_command(self, target_instance_id, commands, comment):
        response = self.ssm_client.send_command(
            InstanceIds=[target_instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': commands},
            Comment=comment
        )

        return response['Command']['CommandId']

    def inst_init_setup(self, target_instance_id):

        commands = ['cd /home/ec2-user && sudo yum install vim git -y && sudo pip3 install numpy && sudo pip3 install boto3 && git clone https://github.com/kign17019999/github-cc.git']
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment='initial setup instance')
        
        return command_id
    
    def inst_init_cloneGit(self, target_instance_id, git_url):
        commands = [f'cd /home/ec2-user && git clone {git_url}']
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment='clone git')
        
        return command_id

    def inst_updateGit(self, target_instance_id, git_url, git_foldName):
        #commands = [f'cd /home/ec2-user/{git_foldName} && git reset --hard HEAD && git pull {git_url}']
        commands = [f'cd /home/ec2-user/ && sudo rm -r github-cc', f'cd /home/ec2-user && git clone {git_url}']
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment='update git')
        
        return command_id

    def start_worker_addition(self, target_instance_id, file_name):
        commands = [f'cd /home/ec2-user/github-cc && nohup python3 {file_name} &']
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment=f'start {file_name}')
        
        return command_id

    def stop_worker_addition(self, target_instance_id, file_name):
        commands = ['kill $(ps aux | grep {} | awk '"'"'{{print $2}}'"'"')'.format(file_name)]
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment=f'stop {file_name}')
        
        return command_id

    def start_worker(self, target_instance_id, file_name, method, queue_url1, region_name1, queue_url2, region_name2, check_queue = None):
        
        commands = [f'cd /home/ec2-user/github-cc && nohup python3 {file_name} {method} {queue_url1} {region_name1} {queue_url2} {region_name2} {check_queue}&']
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment=f'start {file_name}')
        
        return command_id

    def stop_worker(self, target_instance_id, file_name, method, queue_url1, region_name1, queue_url2, region_name2, check_queue = None):
        commands = ['kill $(ps aux | grep {} {} {} {} {} {} {} | awk '"'"'{{print $2}}'"'"')'.format(file_name, method, queue_url1, region_name1, queue_url2, region_name2, check_queue)]
        command_id = self.execute_ssm_command(target_instance_id=target_instance_id, commands=commands, comment=f'stop {file_name}')
        
        return command_id
    

if __name__ == '__main__':
    bt = Boto3Function(region_name = 'us-east-1')
    inst_status = bt.ec2_status()
    for key, value in inst_status.items():
        print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')