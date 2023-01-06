from boto3function import Boto3Function
import time

def evaluate_queue(fileName, method, queue_url1, region_name1, queue_url2, region_name2):
    
    step_spin = 1000
    git_url = 'https://github.com/kign17019999/github-cc.git'
    git_foldName = 'github-cc'
    queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
    always_on = ['CC_Master', 'CC_Worker_01', 'CC_Worker_02']

    b3f = Boto3Function(region_name1)
    # just check worker queue
    num_inQueue = b3f.sqs_check_queue(queue_url)
    inst_dict = b3f.ec2_status()
    print('-----------------------------------------------')
    print('before evaluate queue, the status is followings:')
    print(f'num in queue {num_inQueue}')
    for key, value in inst_dict.items():
        print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')

    if num_inQueue > step_spin:
        inst_dict = b3f.ec2_status()
        for key, value in inst_dict.items():
            #print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
            if value[1] != 'running':
                id_spin = value[0]
                instance_name = key
                status_on = b3f.ec2_start(id_spin)
                while True:
                    inst_dict = b3f.ec2_status()
                    if inst_dict[instance_name][1] == 'running':
                        break
                b3f.start_worker(
                    target_instance_id = id_spin, 
                    file_name = fileName, 
                    method = method, 
                    queue_url1 = queue_url1, 
                    region_name1 = region_name1, 
                    queue_url2 = queue_url2, 
                    region_name2 = region_name2, 
                    check_queue = None
                    )
                
                break
    else:
        inst_dict = b3f.ec2_status()
        for key, value in inst_dict.items():
            if value[1] != 'stopped' and value[1] != 'stopping':
                if key not in always_on:
                    status_off = b3f.ec2_start(value[0])
    
    num_inQueue = b3f.sqs_check_queue(queue_url)
    inst_dict = b3f.ec2_status()
    print('-----------------------------------------------')
    print('after evaluate queue, the result is followings:')
    print(f'num in queue {num_inQueue}')
    for key, value in inst_dict.items():
        print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
    print('-----------------------------------------------')

if __name__ == '__main__':
    evaluate_queue('us-east-1')
    #evaluate_queue()