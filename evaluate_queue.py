from boto3function import Boto3Function
import time

def evaluate_queue(fileName, method, queue_url1, region_name1, queue_url2, region_name2):
    with open('START_CONFIG.txt', 'r') as f:
        lines = f.readlines()
    line = lines[0]
    data = line.split('=')
    keys_and_values = data[1].split(' ')
    result_dict = {}
    for i in range(0, len(keys_and_values), 2):
        result_dict[keys_and_values[i]] = keys_and_values[i+1]

    step_spin = result_dict['step_spin'].rstrip()
    time_for_evaluate = result_dict['time_for_evaluate'].rstrip()

    git_url = result_dict['git_url'].rstrip()
    git_foldName = result_dict['git_foldName'].rstrip()
    always_on = result_dict['always_on'].rstrip()

    b3f = Boto3Function(region_name1)
    # just check worker queue
    num_inQueue = b3f.sqs_check_queue(queue_url1)
    inst_dict = b3f.ec2_status()
    print('-----------------------------------------------')
    print('before evaluate queue, the status is followings:')
    print(f'num in queue {num_inQueue}')
    for key, value in inst_dict.items():
        print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')

    if num_inQueue[1] > int(step_spin):
        inst_dict = b3f.ec2_status()
        for key, value in inst_dict.items():
            #print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
            if value[1] != 'running':
                id_spin = value[0]
                instance_name = key
                status1 = ""
                while status1 != 'yes':
                    try:
                        status_on = b3f.ec2_start(id_spin)
                        status1 = 'yes'
                    except:
                        pass
                while True:
                    inst_dict = b3f.ec2_status()
                    if inst_dict[instance_name][1] == 'running':
                        break
                status1 = ""
                while status1 != 'yes':
                    try:
                        b3f.inst_updateGit(
                            target_instance_id = id_spin, 
                            git_url = git_url, 
                            git_foldName = git_foldName
                            )
                        status1 = 'yes'
                    except:
                        pass
                b3f.inst_init_setup(id_spin)
                b3f.start_worker(
                    target_instance_id = id_spin, 
                    file_name = fileName, 
                    method = method, 
                    queue_url1 = queue_url1, 
                    region_name1 = region_name1, 
                    queue_url2 = queue_url2, 
                    region_name2 = region_name2, 
                    check_queue = None,
                    time_for_evaluate = time_for_evaluate,
                    step_spin= step_spin,
                    git_url= git_url,
                    git_foldName= git_foldName,
                    always_on= always_on
                    )
                
                break
    else:
        inst_dict = b3f.ec2_status()
        for key, value in inst_dict.items():
            if value[1] != 'stopped' and value[1] != 'stopping':
                if key not in always_on:
                    status1 = ""
                    while status1 != 'yes':
                        try:
                            status_off = b3f.ec2_stop(value[0])
                            status1 = 'yes'
                        except:
                            pass
                    
    
    num_inQueue = b3f.sqs_check_queue(queue_url1)
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