import master5mp as m5
import queue_delete_msg as qdm
import result_log as rl
from boto3function import Boto3Function
import time

def main():
    #******************************************************************************

    # design metrix and number of package
    m1 = 5
    n1 = 5
    m2 = 5
    n2 = 5
    partition = (m1*n2)//1

    # config mode
    method = 'addition'
    #method = 'multiplication'
    parallel = False


    # config URL
    queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
    region_name1 = 'us-east-1'
    queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
    region_name2 = 'us-east-1' 

    #******************************************************************************
    #exec(open("ssm_start_w3a.py").read())

    b3f = Boto3Function(region_name1)

    inst_dict = b3f.ec2_status()
    print('-----------------------------------------------')
    for key, value in inst_dict.items():
        print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
    print('-----------------------------------------------')

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
    always_on = [inst_worker_id[1], inst_worker_id[2]]
    start_by_off = [inst_worker_id[3], inst_worker_id[4], inst_worker_id[5], inst_worker_id[6], inst_worker_id[7]]
    id_cowork = [inst_worker_id[1]]
    id_list = [inst_worker_id[2]]
    #id_list = ['i-055336f9cd0657c5c']
    
    fileName = 'worker6.py'
    git_url = 'https://github.com/kign17019999/github-cc.git'
    git_foldName = 'github-cc'
    
    for id in start_by_off:
        status_off = b3f.ec2_stop(id)

    b3f.inst_updateGit(
        target_instance_id = id_cowork, 
        git_url = git_url, 
        git_foldName = git_foldName
        )
    b3f.inst_init_setup(id_cowork)
    b3f.start_worker(
        target_instance_id = id_cowork, 
        file_name = fileName, 
        method = method, 
        queue_url1 = queue_url1, 
        region_name1 = region_name1, 
        queue_url2 = queue_url2, 
        region_name2 = region_name2, 
        check_queue = True
        )
    
    for id in id_list:
        b3f.inst_updateGit(
            target_instance_id = id, 
            git_url = git_url, 
            git_foldName = git_foldName
            )
        b3f.inst_init_setup(id)

    #time.sleep(5)

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
    print('-----------------------------------------------')
    for key, value in inst_dict.items():
        print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
    print('-----------------------------------------------')
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


if __name__ == '__main__':
    main()