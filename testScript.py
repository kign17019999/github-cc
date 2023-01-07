import master5mp as m5
import queue_delete_msg as qdm
import result_log as rl
from boto3function import Boto3Function
import time
import queue_delete_msg

should_stop = 0

import threading

def print_message():
    t = 10
    while should_stop == 0:
        b3f = Boto3Function('us-east-1')
        inst_dict = b3f.ec2_status()
        names = []
        status = []
        print('-----------------------------------------------')
        for key, value in inst_dict.items():
            #print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
            if 'Worker' in key:
                #print(f'Instance name: {key}, Running status: {value[1]}')
                print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
        print('-----------------------------------------------')
        time.sleep(t)
    



def main():
    global should_stop

    #******************************************************************************

    # design metrix and number of package
    m1 = 20
    n1 = m1
    m2 = m1
    n2 = m1
    partition = (m1*n2)//1

    # config mode
    method = 'addition'
    #method = 'multiplication'
    parallel = True


    # config URL
    queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
    region_name1 = 'us-east-1'
    queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
    region_name2 = 'us-east-1' 

    # delete everything inqueue befoer perform command
    queue_delete_msg.delete_msg(queue_url1, region_name1)
    print('finish')
    queue_delete_msg.delete_msg(queue_url2, region_name2)
    print('finish')

    #******************************************************************************
    time.sleep(1)
    b3f = Boto3Function(region_name1)
    inst_dict = b3f.ec2_status()    

    inst_worker_id = {
        '1':'i-0a583c0ad764b4926',
        '2':'i-055336f9cd0657c5c',
        '3':'i-08fa110b2324b11c5',
        '4':'i-0d4f2d3a0d1f239bb',
        '5':'i-0faf62a75a784809a',
        '6':'i-011e5c83dd72ef526',
        '7':'i-0c2111a6e13bc4637',
        '8':'i-068cd621413f03c08'
        }
    always_on = [inst_worker_id['1'], inst_worker_id['2'], inst_worker_id['3']]
    start_by_off = [inst_worker_id['4'], inst_worker_id['5'], inst_worker_id['6'], inst_worker_id['7'], inst_worker_id['8']]
    #start_by_off = []
    id_cowork = [inst_worker_id['1']]
    id_list = [inst_worker_id['2'], inst_worker_id['3']]
    #id_list = ['i-055336f9cd0657c5c']
    
    fileName = 'worker6.py'
    git_url = 'https://github.com/kign17019999/github-cc.git'
    git_foldName = 'github-cc'
    

    for id in always_on:
        status1 = ""
        while status1 != 'yes':
            try:
                status_on = b3f.ec2_start(id)
                status1 = 'yes'
            except:
                pass
        status0 = ""
        while status0 != 'running':
            inst_dict = b3f.ec2_status()  
            for key, value in inst_dict.items():
                if inst_dict[key][0] == id:
                    print(f'waiting {id} : {inst_dict[key][1]}')
                    status0 = inst_dict[key][1]
            time.sleep(1)

    for id in start_by_off:
        status_off = b3f.ec2_stop(id)

    if len(id_cowork) >0:
        status1 = ""
        while status1 != 'yes':
            try:
                b3f.inst_updateGit(
                    target_instance_id = id_cowork[0], 
                    git_url = git_url, 
                    git_foldName = git_foldName
                    )
                status1 = 'yes'
            except:
                pass

        b3f.inst_init_setup(id_cowork[0])
        b3f.start_worker(
            target_instance_id = id_cowork[0], 
            file_name = fileName, 
            method = method, 
            queue_url1 = queue_url1, 
            region_name1 = region_name1, 
            queue_url2 = queue_url2, 
            region_name2 = region_name2, 
            check_queue = True
            )
    
    for id in id_list:
        status1 = ""
        while status1 != 'yes':
            try:
                b3f.inst_updateGit(
                    target_instance_id = id, 
                    git_url = git_url, 
                    git_foldName = git_foldName
                    )
                status1 = 'yes'
            except:
                pass

        b3f.inst_init_setup(id)

    for id in id_list:
        b3f.start_worker(
            target_instance_id = id, 
            file_name = fileName, 
            method = method, 
            queue_url1 = queue_url1, 
            region_name1 = region_name1, 
            queue_url2 = queue_url2, 
            region_name2 = region_name2, 
            check_queue = None
        )

    result = m5.master(
        method = method,
        queue_url1 = queue_url1, 
        region_name1 = region_name1, 
        queue_url2 = queue_url2, 
        region_name2 = region_name2, 
        partition = partition, 
        m1 = m1, 
        n1 = n1, 
        m2 = m2, 
        n2 = n2, 
        randF=0, randT=10, 
        time_before_print_process=5, time_before_resend=15,
        parallel = parallel
    )

    rl.add_or_create_log(
        fileName='system_mp_log.csv',
        fileDir='/home/ec2-user/github-cc/',
        dict_data=result
    )

    #exec(open("ssm_stop_w3a.py").read())
    for id in id_list:
        b3f.stop_worker(
            target_instance_id = id, 
            file_name = fileName, 
            method = method, 
            queue_url1 = queue_url1, 
            region_name1 = region_name1, 
            queue_url2 = queue_url2, 
            region_name2 = region_name2, 
            check_queue = None
        )

    should_stop = 1

if __name__ == '__main__':
    
    thread = threading.Thread(target=print_message)
    thread.start()
    main()