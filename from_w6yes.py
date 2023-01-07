from sqsfunction import SQSFunction
from matrixparallel_v2 import MatrixParallel
import evaluate_queue
import numpy as np
import sys
import time
import __main__

time_before_evaluate_queue = 10

def worker(method, queue_url1, region_name1, queue_url2, region_name2, check_queue = None):
    #print(f'check_queue = {check_queue}')
    sqs_function1 = SQSFunction(queue_url1, region_name1)
    sqs_function2 = SQSFunction(queue_url2, region_name2)

    # metrix operation
    mp = MatrixParallel()

    print(f'acting as a {method} worker')
    print('start receving & processing & send to master_queue...')
    count = 0
    start_time = time.time()
    while True:
        message = sqs_function1.receive_message()
        if message is not None:
            num_in_msg = len(message)
            results = []
            for j in range(num_in_msg):
                if method == 'addition':
                    one_result = mp.addition(message[j])
                elif method == 'multiplication':
                    one_result = mp.multiplication(message[j])
                results.append(one_result)
            message_id = sqs_function2.send_message(message=results)
            count+=1
            print(f'    {count}: Done process & Sent result with msg_id: {message_id}')
        if check_queue == str(True):
            if time.time() - start_time > time_before_evaluate_queue:
                evaluate_queue.evaluate_queue(str(__main__.__file__), method, queue_url1, region_name1, queue_url2, region_name2)
                start_time = time.time()
                if __name__ == '__main__':

if __name__ == '__main__':

    try:
        method = sys.argv[1]
        check_queue = sys.argv[2]
        worker(
            method = method,
            queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker',
            region_name1 = 'us-east-1',
            queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master',
            region_name2 = 'us-east-1' ,
            check_queue = check_queue
            )
    except:
        with open('dict_file.txt', 'r') as f:
            lines = f.readlines()
        line = lines[0]
        data = line.split('=')
        keys_and_values = data[1].split(' ')
        result_dict = {}
        for i in range(0, len(keys_and_values), 2):
            result_dict[keys_and_values[i]] = keys_and_values[i+1]

        worker(
            method = result_dict['method'],
            queue_url1 = result_dict['queue_url1'],
            region_name1 = result_dict['region_name1'],
            queue_url2 = result_dict['queue_url2'],
            region_name2 = result_dict['region_name2'],
            check_queue = result_dict['check_queue']
            )













################

from boto3function import Boto3Function
import time

def evaluate_queue(fileName, method, queue_url1, region_name1, queue_url2, region_name2):

    step_spin = 0
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

    if num_inQueue[1] >= step_spin:
        inst_dict = b3f.ec2_status()
        for key, value in inst_dict.items():
            #print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
            if value[1] != 'running':
                id_spin = value[0]
                instance_name = key
                print(f'try to on {key}')
                status_on = b3f.ec2_start(id_spin)
                while True:
                    inst_dict = b3f.ec2_status()
                    print(inst_dict[instance_name][1])
                    time.sleep(1)
                    if inst_dict[instance_name][1] == 'running':
                        break
                print(f'try to update git')
                try:
                    print(id_spin)
                    print(type(id_spin))
                    b3f.inst_updateGit(
                        target_instance_id = 'i-055336f9cd0657c5c',
                        git_url = git_url,
                        git_foldName = git_foldName
                        )
                except Exception as e:
                    print('fial update git')
                    print(e)
                print(f'try to init')
                b3f.inst_init_setup(id_spin)
                print(f'try to start w')
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
            print('done')
    else:
        inst_dict = b3f.ec2_status()
        for key, value in inst_dict.items():
            if value[1] != 'stopped' and value[1] != 'stopping':
                if key not in always_on:
                    status_off = b3f.ec2_stop(value[0])

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
                                                                                                         