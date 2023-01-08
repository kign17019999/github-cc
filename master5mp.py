from sqsfunction import SQSFunction
from matrixparallel_v2 import MatrixParallel
from boto3function import Boto3Function
import queue_delete_msg
import numpy as np
import time
import multiprocessing
import __main__

'''
This python file has 'master function' as a main (which call from if __name__ == '__main__')
There are 3 sub functions to proform metrix operatin and sending to distributed system over AWS SQS following,
    - decompose_mat = decompose metrix from 2 given metrix2
    - send_msg = send decomposed metrix into SQS Queue
    - get_results = obtain teh result from SQS Queue (which refer to decompose_mat in previous step)

HOW TO USE:
    - run this file directly w/o any input >> it will print the result of metrix addition by defualt setting
    - import this file and use 'master method' to compute desired redomed metrix by following example
        >> import fileName (.py)
        >> my_class = fileName.master(
                method = 'addidtion',
                queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker', 
                region_name1 = 'us-east-1', 
                queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master', 
                region_name2 = 'us-east-1', 
                partition = 10, 
                m1 = 10, 
                n1 = 10, 
                m1 = 10, 
                n1 = 10, 
                randF=0, randT=10, 
                time_before_print_process=5, time_before_resend=15,
                parallel = False
            )
'''

def master(method, queue_url1, region_name1, queue_url2, region_name2, partition=10, m1=10, n1=10, m2=10, n2=10, randF=0, randT=10, time_before_print_process=5, time_before_resend=15, parallel=False):
    print('* * * * * start * * * * *')
    print(f'run fom :{__main__.__file__}')
    print(f'Starting Distributed Cloud System to perform a matrix {method} ...')

    # delete everything inqueue befoer perform command
    #queue_delete_msg.delete_msg(queue_url1, region_name1)
    #print('    Finish')
    #queue_delete_msg.delete_msg(queue_url2, region_name2)
    #print('    Finish')

    # metrix operation
    start_gen_mat = time.time()
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m1,n1,randF,randT)
    mat2 = mp.gen_matrix(m2,n2,randF,randT)
    time_for_gen_mat = time.time() - start_gen_mat

    # timing overall process by distributed system
    start_time_all = time.time()

    print('start decompose metrix..')
    pack_of_matrixs, dict_of_matrixs, time_for_decompose = decompose_mat(method, mp, mat1, mat2, partition, time_before_print_process)

    if parallel == False:
        print('start sending..')
        time_for_sending = send_msg(method, m1, n1, m2, n2, partition, time_before_print_process, pack_of_matrixs, queue_url1, region_name1)

        print('start getting result & combine...')
        final_result, time_for_getting_result, log_during_combining = get_results(method, mp, dict_of_matrixs, time_before_resend, time_before_print_process, partition, queue_url1, region_name1, queue_url2, region_name2)

    elif parallel == True:
        # create a pool of worker processor
        pool = multiprocessing.Pool(2)
        
        print('start sending... (using Parallel CPU core at Master)')
        temp_send = pool.apply_async(send_msg, (method, m1, n1, m2, n2, partition, time_before_print_process, pack_of_matrixs, queue_url1, region_name1))

        print('start getting result & combine... (using Parallel CPU core at Master)')
        temp_get = pool.apply_async(get_results,(method, mp, dict_of_matrixs, time_before_resend, time_before_print_process, partition, queue_url1, region_name1, queue_url2, region_name2))
    
        # waiting for finish all worker processor and join
        pool.close()
        pool.join()

        # getting the return from each parallel function
        time_for_sending = temp_send.get()
        final_result, time_for_getting_result, log_during_combining = temp_get.get()

    # stop timing overall process by distributed system
    stop_time_all = time.time()

    # timing overall process by local system
    start_time_local = time.time()
    if method == 'addition':
        result_with_local = np.add(mat1,mat2)
    elif method == 'multiplication':
        result_with_local = np.dot(mat1,mat2)
    
    # stoptiming overall process by local system
    stop_time_local = time.time()
    print('-----------------------------------------------')
    print('checking result:')
    print(f'{final_result == result_with_local}')
    print('-----------------------------------------------')
    print('timing...')
    parallel_word = ""
    if parallel == True: parallel_word = "(Parallel CPU core) "
    print('-----------------------------------------------')
    print(f'>> total time gen 2 matrics     : {time_for_gen_mat} s')
    print('-----------------------------------------------')
    print(f'>> total time decompose         : {time_for_decompose} s')
    print(f'>> total time sending message   : {time_for_sending} s {parallel_word}')
    print(f'>> total time getting result    : {time_for_getting_result} s (include resending time) {parallel_word}')
    print('-----------------------------------------------')
    print(f'>> total time distibuted system : {stop_time_all-start_time_all} s {parallel_word}')
    print(f'>> total time local system      : {stop_time_local-start_time_local} s')
    print('-----------------------------------------------')

    print('-----------------------------------------------')
    np.savetxt("result_dist.csv", final_result, delimiter=",", fmt="%.3f")
    np.savetxt("result_local.csv", result_with_local, delimiter=",", fmt="%.3f")
    print(f'>> saving latest dist-result in  "result_dist.csv"')
    print(f'>> saving latest dist-result in  "result_local.csv"')
    print('-----------------------------------------------')
    print('* * * * * end * * * * *')
    
    #log_during_combining = [log_msg_in_queue_worker, log_msg_in_queue_master, log_num_instance, log_time]
    return_data = {
        'method': method,
        'mat1_size': f'{m1}x{n1}',
        'mat2_size': f'{m2}x{n2}',
        'num_packages': partition,
        'master_multiprocess': parallel,
        'total_time_gen_mat': time_for_gen_mat,
        'total_time_local': stop_time_local-start_time_local,
        'total_time_dist': stop_time_all-start_time_all,
        'time_decompose': time_for_decompose,
        'time_sending': time_for_sending,
        'time_combining': time_for_getting_result,
        'log_msg_in_queue_worker': log_during_combining[0],
        'log_msg_in_queue_master': log_during_combining[1],
        'log_num_instance': log_during_combining[2],
        'log_time': log_during_combining[3]
        }
    return return_data

def decompose_mat(method, mp, mat1, mat2, partition, time_before_print_process):
    '''
    This function will decompose two given metrix into a list with index
    Input:
        - method = selection method between 'addition' and 'multiplication'
        - mp = an instance of that class 'metrixparallel.py' (should be used this instances untill ending the process because each method in class will use same slef.argument)
        - mat1 = matrix1
        - mat2 = matrix2
        - partition = number of package that user want to send
        - time_before_print_process =  = setting time before updating grogress of process (print out) (in s)
    return:
        - pack_of_matrixs = list of packgage containing index and decomposed metrix (for being a message sending)
        - dict_of_matrixs = dicct of package containing index and decomposed metrix (for being a result obtaining)
        - time_for_decompose = time that use for decomposing process
    '''
    # timing be priting the progress
    start_time_for_decompose= time.time()

    if method == 'addition':
        # decompose and priting
        pack_of_matrixs, dict_of_matrixs = mp.decompose_for_addition(mat1, mat2, partition, time_before_print_process)
    elif method == 'multiplication':
        # decompose and priting
        pack_of_matrixs, dict_of_matrixs = mp.decompose_for_multiplication(mat1, mat2, partition, time_before_print_process)
    
    stop_time_for_decompose= time.time()

    # summary decomposing time
    time_for_decompose = stop_time_for_decompose - start_time_for_decompose

    return pack_of_matrixs, dict_of_matrixs, time_for_decompose

def send_msg(method, m1, n1, m2, n2, partition, time_before_print_process, pack_of_matrixs, queue_url1, region_name1):
    '''
    this function will send the message through AWS SQS
    Input:
        - method = selection method between 'addition' and 'multiplication'
        - m1 = number of ROW of metrix1
        - n1 = number of COLUMN of metrix1
        - m2 = number of ROW of metrix2
        - n2 = number of COLUMN of metrix2
        - partition = number of package that user want to send
        - time_before_print_process = setting time before updating grogress of process (print out) (in s)
        - pack_of_matrixs = list of packgage containing index and decomposed metrix (for being a message sending)
        - queue_url1 = URL of AWS SQS that this function will send to
        - region_name1 = Region Name of AWS SQS that this function will send to
    return:
        - time_for_sending = time that use for sending process
    '''
    # create instance of SQS Class
    sqs_function1 = SQSFunction(queue_url1, region_name1)

    # check number of metrix operation each method
    if method == 'addition':
        num_operation = m1
    elif method == 'multiplication':
        num_operation = m1*n2

    if m1 >= partition:
        min_msg_each_send = num_operation//partition
        max_msg_each_send = min_msg_each_send+1
        num_send_with_max = num_operation%partition
    else:
        min_msg_each_send = 1
        max_msg_each_send = 1
        num_send_with_max = 0
    
    start_time_for_sending = time.time()
    
    # timing be priting the progress
    start_time = time.time()

    # create pointer that will point to decomposed metrix that will be pack into message's package
    num_in_pack_of_matrixs = 0
    
    # looping through the number of package that user want to send
    for i in range(partition):
        # create parameter to store list of decomposed package that will be in each sending time (1 time sending)
        set_pack_of_matrixs = []
        
        # define the number of decomposed metrix each message
        if num_send_with_max != 0 :
            num_in_msg = max_msg_each_send
            num_send_with_max-=1
        else:
            num_in_msg = min_msg_each_send
        
        # add decomposed metrix into 'set_pack_of_matrixs'
        for round in range(num_in_msg):
            one_pack_of_matrixs = pack_of_matrixs[num_in_pack_of_matrixs]
            set_pack_of_matrixs.append(one_pack_of_matrixs)
            num_in_pack_of_matrixs+=1
        
        # send the message over SQS
        message_id = sqs_function1.send_message(message = set_pack_of_matrixs)
        
        # checking the time before print progress
        if time.time()-start_time > time_before_print_process:
            start_time = time.time()
            print(f'    (SEND) trying to send...{i}/{partition} pakages')
    
    stop_time_for_sending = time.time()
    print(f'    (SEND) finishing sending...{partition}/{partition} pakages')

    # summary sending time
    time_for_sending = stop_time_for_sending - start_time_for_sending

    return time_for_sending

def get_results(method, mp, dict_of_matrixs, time_before_resend, time_before_print_process, partition, queue_url1, region_name1, queue_url2, region_name2):
    '''
    This function will get all of the sub_result from AWS SQS according to 'dict_of_matrixs' which created when decomposing metrix
    during getting process, the function also combine the sub_result into the result
    Input:
        - method  = selection method between 'addition' and 'multiplication'
        - mp = an instance of that class 'metrixparallel.py' (should be used this instances untill ending the process because each method in class will use same slef.argument)
        - dict_of_matrixs = dicct of package containing index and decomposed metrix (for being a result obtaining) 
        - time_before_resend = setting time that this function will be wait before resend the decomposed metrix to re calculation in case of having no result for a long time in SQS
        - time_before_print_process = setting time before updating grogress of process (print out) (in s)
        - partition = number of package that user want to send
        - queue_url1 = URL of AWS SQS that this function will retrive the decomposed metrix (get metrix)
        - region_name1 = Region Name of AWS SQS that this function will retrive the decomposed metrix (get metrix)
        - queue_url2 = URL of AWS SQS that this function will send to (send result)
        - region_name2 = Region Name of AWS SQS that this function will send to (send result)
    return:
        - final_result = combined result from sub-result
        - time_for_getting_result = time that use for getting result process
    '''

    # create instance of SQS Class for receiving and sending, respectively
    sqs_function1 = SQSFunction(queue_url1, region_name1)
    sqs_function2 = SQSFunction(queue_url2, region_name2)
    
    # timeing getting process
    start_time_getting_result = time.time()

    # timing be priting the progress
    start_time = time.time()
    start_time_progress = time.time()

    # timing before resending process
    no_msg_time = time.time()
    
    # setting the couting number for priting the progress
    count_get = 0
    count_get_result = 0
    
    want_result = len(dict_of_matrixs)
    
    b3f = Boto3Function('us-east-1')
    log_msg_in_queue_worker = []
    log_msg_in_queue_master = []
    log_num_instance = []
    log_time = []

    # looping for getting result
    while True:
        # read message from SQS Queue
        message = sqs_function2.receive_message()
        
        # if it has message >> combining result and delete it from 'dict_of_matrixs'
        if message is not None:
            for one_result in message:
                #print(one_result)
                index = one_result[0][0]
                sub_index = one_result[1][0]
                ikey = f'{index}-{sub_index}'
                if ikey in dict_of_matrixs:
                    if method == 'addition':
                        status_combine = mp.combine_addition(one_result)
                    elif method == 'multiplication':
                        status_combine = mp.combine_multiplication(one_result)
                    del dict_of_matrixs[ikey]
                    count_get_result +=1
            # update counting progress
            count_get+=1

            # timing before resending process (reset after getting first msg)
            no_msg_time = time.time()
        # check no msg time before resending
        if time.time()-no_msg_time > time_before_resend:
            print(f'    !! no message for {time_before_resend}s, try to check the blank result in Dict_Matrix')
            # timing for update progress of resending with counting too
            start_time_resend = time.time()            
            count_resend = 0
            count_num_for_resend = len(dict_of_matrixs)
            for key, value in dict_of_matrixs.items():
                one_pack_of_matrixs = value
                #print(one_pack_of_matrixs)
                message_id = sqs_function1.send_message(message = [one_pack_of_matrixs])
                count_resend+=1
                if time.time()-start_time_resend > time_before_print_process:
                    start_time_resend = time.time()
                    print(f'        (RESENT) trying to resending...{count_resend}/{count_num_for_resend} sub-pair')
            print(f'        (RESENT) finish resending...{count_resend}/{count_num_for_resend} sub-pair')
            if count_resend > 0:
                # timing before resending process (reset after finish previous resend)
                no_msg_time = time.time()
            else:
                break

        # check time before update the progress
        if time.time()-start_time > time_before_print_process:
            start_time = time.time()
            print(f'    (GET) trying to get results...{count_get}/{partition} packages | {count_get_result}/{want_result} sub-result')
            
            inst_dict = b3f.ec2_status()
            num_running_instance = 0
            num_starting_instance = 0
            for key, value in inst_dict.items():
                if 'Worker' in key and value[1] == 'running':
                    num_running_instance +=1
                if 'Worker' in key and value[1] == 'pending':
                    num_starting_instance +=1
            num_inQueue_worker = b3f.sqs_check_queue(queue_url1)
            num_inQueue_master = b3f.sqs_check_queue(queue_url2)

            log_msg_in_queue_worker.append(num_inQueue_worker[1])
            log_msg_in_queue_master.append(num_inQueue_master[1])
            log_num_instance.append(num_running_instance)
            log_time.append(start_time)

            if time.time() - start_time_progress > time_before_resend:
                print('----------------------------------------------------------------------------------------')
                print(f'* {num_running_instance} workers are running')
                print(f'* {num_starting_instance} workers try to start')
                print(f'* {num_inQueue_worker[1]} msg to worker')
                print(f'* {num_inQueue_master[1]} msg to master')
                print('----------------------------------------------------------------------------------------')
                start_time_progress = time.time()
                

        # check if all of get equal to number of package >> break the loop (because it is done)
        if len(dict_of_matrixs) == 0:
            break
    
    stop_time_getting_result = time.time()
    print(f'    (GET) finish getting all result & combining...{count_get}/{partition} packages | {count_get_result}/{want_result} sub-result') 

    time_for_getting_result = stop_time_getting_result - start_time_getting_result

    # summary getting result time
    if method == 'addition':
        final_result = mp.get_result_addition()
    elif method == 'multiplication':
        final_result = mp.get_result_multiplication()

    inst_dict = b3f.ec2_status()
    num_running_instance = 0
    num_starting_instance = 0
    for key, value in inst_dict.items():
        if 'Worker' in key and value[1] == 'running':
            num_running_instance +=1
        if 'Worker' in key and value[1] == 'pending':
            num_starting_instance +=1
    num_inQueue_worker = b3f.sqs_check_queue(queue_url1)
    num_inQueue_master = b3f.sqs_check_queue(queue_url2)

    log_msg_in_queue_worker.append(num_inQueue_worker[1])
    log_msg_in_queue_master.append(num_inQueue_master[1])
    log_num_instance.append(num_running_instance)
    log_time.append(start_time) 
    print('----------------------------------------------------------------------------------------')
    print(f'* {num_running_instance} workers are running')
    print(f'* {num_starting_instance} workers try to start')
    print(f'* {num_inQueue_worker[1]} msg to worker')
    print(f'* {num_inQueue_master[1]} msg to master')
    print('----------------------------------------------------------------------------------------')
    start_time_progress = time.time()
    log_during_combining = [log_msg_in_queue_worker, log_msg_in_queue_master, log_num_instance, log_time]

    return final_result, time_for_getting_result, log_during_combining

if __name__ == '__main__':
    result = master(
        method = 'addition',
        queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker', 
        region_name1 = 'us-east-1', 
        queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master', 
        region_name2 = 'us-east-1', 
        partition = 10, 
        m1 = 10, 
        n1 = 10, 
        m2 = 10, 
        n2 = 10, 
        randF=0, randT=10, 
        time_before_print_process=5, time_before_resend=15,
        parallel = False
        )
    print(f'result: {result}')
