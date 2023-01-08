import master5mp as m5
import queue_delete_msg as qdm
import result_log as result_log
from boto3function import Boto3Function
import time
import queue_delete_msg
import ast
#import threading
import sys

global file_name, queue_url1, region_name1, queue_url2, region_name2, time_for_evaluate, step_spin, git_url, git_foldName
global randF, randT, time_before_print_process, time_before_resend, parallel
global spare_workerid, special_workerid, normal_workerid, always_on

#stop_print_instance_status = 1
    
def main(method, m1, n1, m2, n2, partition):
    #global stop_print_instance_status
    time.sleep(2)
    print('-----------------------------------------------')
    # delete everything inqueue befoer perform command
    queue_delete_msg.delete_msg(queue_url1, region_name1)
    queue_delete_msg.delete_msg(queue_url2, region_name2)

    print('stop all spare_worker...')
    for id in spare_workerid:
        TE_stopEC2(id)

    print('start and run special worker...')
    if len(special_workerid) >0:
        for id in special_workerid:
            TE_stopW(id)
            TE_startEC2(id)
            TE_startW(id, method, True)
    
    print('start and run normal worker...')
    for id in normal_workerid:
        TE_stopW(id)
        TE_startEC2(id)
        TE_startW(id, method, None)

    #stop_print_instance_status = 1

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


    #stop_print_instance_status = 1

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
            break

def TE_startEC2(id):
    b3f = Boto3Function(region_name1)
    status = ""
    while status != 'yes':
        try:
            status_on = b3f.ec2_start(id)
            status = 'yes'
        except Exception as e:
            print(e)

    status = ""
    while status != 'running':
        inst_dict = b3f.ec2_status()  
        for key, value in inst_dict.items():
            if inst_dict[key][0] == id:
                print(f'waiting {id} : {inst_dict[key][1]}')
                status = inst_dict[key][1]
                time.sleep(1)

def TE_stopEC2(id):
    b3f = Boto3Function(region_name1)
    status_on = b3f.ec2_stop(id)
    '''
    status = ""
    while status != 'yes':
        try:
            status_on = b3f.ec2_stop(id)
            status = 'yes'
        except:
            pass
    '''

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
    print('----------------------------------------------------------------------------------------')
    print(f'spare_workerid  : {spare_workerid}')
    print(f'special_workerid: {special_workerid}')
    print(f'normal_workerid : {normal_workerid}')
    print(f'always_on : {always_on}')
    print(f'step-msg to spin new worker : more than {step_spin} msgs in Queue')

def print_instance_status():
    b3f = Boto3Function('us-east-1')
    inst_dict = b3f.ec2_status()
    print('----------------------------------------------------------------------------------------')
    for key, value in inst_dict.items():
        if 'Worker' in key:
            print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
    print('----------------------------------------------------------------------------------------')

    while stop_print_instance_status == 1:
        pass
    start_time = time.time()
    while stop_print_instance_status == 0:
        inst_dict = b3f.ec2_status()
        print('----------------------------------------------------------------------------------------')
        for key, value in inst_dict.items():
            if 'Worker' in key:
                print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
        print('----------------------------------------------------------------------------------------')
        if(time.time()-start_time>time_before_resend):
            print('----------------------------------------------------------------------------------------')
            for key, value in inst_dict.items():
                if 'Worker' in key:
                    print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
            print('----------------------------------------------------------------------------------------')
            start_time = time.time()

def input_function(text_to_inpit):
    # Keep prompting the user for input until they enter a non-empty string
    while True:
        user_input = input(f"{text_to_inpit}: ")
        if user_input.strip():  # Check if the string is not just whitespace
            break
        else:
            break
    return user_input

if __name__ == '__main__':
    
    import_config()
    b3f = Boto3Function('us-east-1')
    inst_dict = b3f.ec2_status()
    print('----------------------------------------------------------------------------------------')
    for key, value in inst_dict.items():
        if 'Worker' in key:
            print(f'Instance name: {key}, Instance ID: {value[0]}, Running status: {value[1]}')
    print('----------------------------------------------------------------------------------------')
    #thread = threading.Thread(target=print_instance_status)
    #thread.start()
    #main()
    

    try:
        method = sys.argv[1]
        m1 = sys.argv[2]
        n1 = sys.argv[3]
        m2 = sys.argv[4]
        n2 = sys.argv[5]
        partition = sys.argv[6]
        main(method, m1, n1, m2, n2, partition)

    except:
        print('Welcome to our appliaction')
        while True:
            method_str = input_function('INPUT "addition" or "multiplication"')
            if method_str == 'addition' or method_str == 'multiplication':
                break
        while True:
            m1_str = input_function('INPUT a number of ROW size of matrix 1 (m1)')
            if m1_str.isdigit():
                break
        while True:
            n1_str = input_function('INPUT a number of COLUMN size of matrix 1 (n1)')
            if n1_str.isdigit():
                break
        if method_str == 'addition':
            m2_str = m1_str
            n2_str = m1_str
            print('m2 and n2 or matrix 2 are forced to be the same with Matrix 1')
        else:
            m2_str = n1_str
            print('m2 matrix 2 is forced to be the same with n1 of Matrix 1')
            while True:
                n2_str = input_function('INPUT a number of COLUMN size of matrix 2 (n2)')
                if n2_str.isdigit():
                    break
        while True:
            parition_str = input_function('INPUT a number of desired number of packages')
            if parition_str.isdigit():
                break

        method = method_str
        m1 = int(m1_str)
        n1 = int(n1_str)
        m2 = int(m2_str)
        n2 = int(n2_str)
        parition = int(parition_str)
        print(type(parition))
        print(type(m2))
        main(method, m1, n1, m2, n2, partition)