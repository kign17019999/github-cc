import master5mp as m5
import queue_delete_msg as qdm
import result_log as result_log
from boto3function import Boto3Function
import time
import queue_delete_msg
import ast
import threading

global file_name, queue_url1, region_name1, queue_url2, region_name2, time_for_evaluate, step_spin, git_url, git_foldName
global randF, randT, time_before_print_process, time_before_resend, parallel
global spare_workerid, special_workerid, normal_workerid, always_on

stop_print_instance_status = 0
    
def main():
    global stop_print_instance_status

    time.sleep(2)

    m1 = 50
    n1 = m1
    m2 = m1
    n2 = m1
    partition = 10000
    method = 'multiplication'

    print('-----------------------------------------------')
    # delete everything inqueue befoer perform command
    queue_delete_msg.delete_msg(queue_url1, region_name1)
    print('    finish')
    queue_delete_msg.delete_msg(queue_url2, region_name2)
    print('    finish')

    for id in spare_workerid:
        TE_stopEC2(id)

    if len(special_workerid) >0:
        for id in special_workerid:
            TE_stopW(id)
            TE_startEC2(id)
            TE_startW(id, method, True)
    
    for id in normal_workerid:
        TE_stopW(id)
        TE_startEC2(id)
        TE_startW(id, method, None)

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
        randF = randF,
        randT = randT, 
        time_before_print_process = time_before_print_process,
        time_before_resend = time_before_resend,
        parallel = parallel
    )

    result_log.add_or_create_log(
        fileName='system_mp_log.csv',
        fileDir='/home/ec2-user/github-cc/',
        dict_data=result
    )

    print('-----------------------------------------------')
    # delete everything inqueue befoer perform command
    queue_delete_msg.delete_msg(queue_url1, region_name1)
    print('    finish')
    queue_delete_msg.delete_msg(queue_url2, region_name2)
    print('    finish')


    stop_print_instance_status = 1

def TE_startW(id, method, check_queue):
    b3f = Boto3Function(region_name1)
    status =""
    while status != 'yes':
        try:
            b3f.inst_updateGit(
                target_instance_id = id, 
                git_url = git_url, 
                git_foldName = git_foldName
            )
            status = 'yes'
        except:
            pass

    time.sleep(1)
    status =""
    while status != 'yes':
        try:
            b3f.inst_init_setup(id)
            status = 'yes'
        except:
            pass

    time.sleep(1)
    status = ""
    while status != 'yes':
        try:
            b3f.start_worker(
                target_instance_id = id, 
                file_name = file_name, 
                method = method, 
                queue_url1 = queue_url1, 
                region_name1 = region_name1, 
                queue_url2 = queue_url2, 
                region_name2 = region_name2, 
                check_queue = check_queue,
                time_for_evaluate = time_for_evaluate,
                step_spin= step_spin,
                git_url= git_url,
                git_foldName= git_foldName,
                always_on= always_on
            )
            status = 'yes'
        except:
            pass

def TE_stopW(id):
    b3f = Boto3Function(region_name1)
    status = ""
    while status != 'yes':
        try:
            b3f.stop_worker(
                target_instance_id = id, 
                file_name = file_name, 
            )
            status = 'yes'
        except:
            pass

def TE_startEC2(id):
    b3f = Boto3Function(region_name1)
    status = ""
    while status != 'yes':
        try:
            status_on = b3f.ec2_start(id)
            status = 'yes'
        except:
            pass

    status = ""
    while status != 'running':
        inst_dict = b3f.ec2_status()  
        for key, value in inst_dict.items():
            if inst_dict[key][0] == id:
                print(f'waiting {id} : {inst_dict[key][1]}')
                status = inst_dict[key][1]

def TE_stopEC2(id):
    b3f = Boto3Function(region_name1)
    status = ""
    while status != 'yes':
        try:
            status_on = b3f.ec2_stop(id)
            status = 'yes'
        except:
            pass


def import_config():

    global stop_print_instance_status
    global file_name
    global queue_url1, region_name1, queue_url2, region_name2
    global time_for_evaluate, step_spin
    global git_url, git_foldName
    global always_on
    global randF
    global randT
    global time_before_print_process
    global time_before_resend
    global parallel
    global spare_workerid
    global special_workerid
    global normal_workerid
    global always_on

    # Open the file in read mode
    with open('config.conf', 'r') as f:
        # Read the lines of the file into a list
        lines = f.readlines()

    # Initialize an empty dictionary to store the parameters
    params = {}

    # Iterate over the lines in the file
    for line in lines:
        # Split the line into a list of words
        words = line.split("=")

        # Extract the parameter name and value from the words
        param_name = words[0]
        param_value = words[1]

        # Strip the quotes from the value, if necessary
        if param_value[0] == "'" or param_value[0] == '"':
            param_value = param_value[1:-1]

        # Convert the value to the appropriate data type
        if param_value == "True":
            param_value = True
        elif param_value == "False":
            param_value = False
        elif param_value.isdigit():
            param_value = int(param_value)
        else:
            try:
                # Use ast.literal_eval to try to parse the value as a list
                param_value = ast.literal_eval(param_value)
            except:
                # If ast.literal_eval raises a ValueError, treat the value as a string
                param_value=param_value[:-1]

        # Add the parameter to the dictionary
        params[param_name] = param_value

    file_name = params['file_name']
    queue_url1 = params['queue_url1']
    region_name1 = params['region_name1']
    queue_url2 = params['queue_url2']
    region_name2 = params['region_name2']
    time_for_evaluate = params['time_for_evaluate']
    step_spin = params['step_spin']
    git_url = params['git_url']
    git_foldName = params['git_foldName']
    always_on = params['always_on']

    randF = params['randF']
    randT = params['randT']
    time_before_print_process = params['time_before_print_process']
    time_before_resend = params['time_before_resend']
    parallel = params['parallel']

    spare_workerid = params['spare_workerid']
    special_workerid = params['special_workerid']
    normal_workerid = params['normal_workerid']
    always_on = params['always_on']

    print(f'spare_workerid  : {spare_workerid}')
    print(f'special_workerid: {special_workerid}')
    print(f'normal_workerid : {normal_workerid}')

def print_instance_status():
    while stop_print_instance_status == 0:
        b3f = Boto3Function('us-east-1')
        inst_dict = b3f.ec2_status()
        print('----------------------------------------------------------------------------------------')
        for key, value in inst_dict.items():
            #print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
            if 'Worker' in key:
                print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
        print('----------------------------------------------------------------------------------------')
        time.sleep(time_before_resend)

if __name__ == '__main__':
    import_config()
    thread = threading.Thread(target=print_instance_status)
    thread.start()
    main()