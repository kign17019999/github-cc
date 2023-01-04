from sqsfunction import SQSFunction
from matrixparallel_v2 import MatrixParallel
import numpy as np
import time

def master_addition(queue_url1, region_name1, queue_url2, region_name2, partition, m, n, randF=0, randT=10, time_before_print_process=5, time_before_resend=15):
    
    sqs_function1 = SQSFunction(queue_url1, region_name1)
    sqs_function2 = SQSFunction(queue_url2, region_name2)

    print('acting as a master addition')




    # metrix operation
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m,n,randF,randT)
    mat2 = mp.gen_matrix(m,n,randF,randT)

    # count all time process
    start_time_all = time.time()


    print('start decompose metrix..')
    pack_of_matrixs, dict_of_matrixs, start_time_for_decompose, stop_time_for_decompose = decompose(mp=mp, mat1=mat1, mat2=mat2, partition=partition)


    
    print('start sending..')
    start_time_for_sending, stop_time_for_sending = send_msg(sqs_function1=sqs_function1, m=m, partition=partition, time_before_print_process=time_before_print_process, pack_of_matrixs=pack_of_matrixs)

    
    
    print('start getting result & combine...')
    final_result, start_time_getting_result, stop_time_getting_result = get_results(mp=mp, sqs_function1=sqs_function1, sqs_function2=sqs_function2, dict_of_matrixs=dict_of_matrixs, time_before_resend=time_before_resend, time_before_print_process=time_before_print_process, partition=partition)

    
    stop_time_all = time.time()

    start_time_local = time.time()
    result_with_local = mat1+mat2
    stop_time_local = time.time()
    
    print('checking result:')
    print(f'{final_result == result_with_local}')
    
    print('timing...')

    print('-----------------------------------------------')
    print(f'>> total time decompose       : {stop_time_for_decompose-start_time_for_decompose} s')
    print(f'>> total time sending message : {stop_time_for_sending-start_time_for_sending} s')
    print(f'>> total time getting result  : {stop_time_getting_result-start_time_getting_result} s (include resending time)')
    print('-----------------------------------------------')
    print(f'>> total time distibuted system    : {stop_time_all-start_time_all} s')
    print(f'>> total time local system         : {stop_time_local-start_time_local} s')
    

def decompose(mp, mat1, mat2, partition):
    # count decomposing time process
    start_time_for_decompose= time.time()

    # initial some parameter for following process
    pack_of_matrixs, dict_of_matrixs = mp.decompose_for_addition(mat1, mat2, partition)
    print(f'finishing decompose into {mp.decomp_count_add}/{partition} parition')
    
    stop_time_for_decompose= time.time()

    return pack_of_matrixs, dict_of_matrixs, start_time_for_decompose, stop_time_for_decompose

def send_msg(sqs_function1, m, partition, time_before_print_process, pack_of_matrixs):
    #check partitoin and num_row_of_metrix
    if m >= partition:
        #this mean sub_metrix from CLASS will be more than num_given parition
        min_msg_each_send = m//partition
        max_msg_each_send = min_msg_each_send+1
        num_send_with_max = m%partition
    else:
        min_msg_each_send = 1
        max_msg_each_send = min_msg_each_send
        num_send_with_max = 0
    
    # count sending time process
    start_time_for_sending = time.time()
    
    # initial some parameter for following process
    start_time = time.time()
    num_in_pack_of_matrixs = 0
    for i in range(partition):
        set_pack_of_matrixs = []
        if num_send_with_max != 0 :
            num_in_msg = max_msg_each_send
            num_send_with_max-=1
        else:
            num_in_msg = min_msg_each_send
        for j in range(num_in_msg):
            one_pack_of_matrixs = pack_of_matrixs[num_in_pack_of_matrixs]
            set_pack_of_matrixs.append(one_pack_of_matrixs)
            num_in_pack_of_matrixs+=1
        message_id = sqs_function1.send_message(message = set_pack_of_matrixs)
        if time.time()-start_time > time_before_print_process:
            start_time = time.time()
            print(f'    trying to sending...{i}/{partition} ')
    
    stop_time_for_sending = time.time()
    print(f'finishing sending...{partition}/{partition} ')

    return start_time_for_sending, stop_time_for_sending

def get_results(mp, sqs_function1, sqs_function2, dict_of_matrixs, time_before_resend, time_before_print_process, partition):
    # count sending time process
    start_time_getting_result = time.time()

    # initial some parameter for following process
    start_time = time.time()
    no_msg_time = time.time()
    count_get = 0
    while True:
        message = sqs_function2.receive_message()
        if message is not None:
            for one_result in message:
                #print(one_result)
                index = one_result[0][0]
                sub_index = one_result[1][0]
                ikey = f'{index}-{sub_index}'
                if ikey in dict_of_matrixs:
                    status_combine = mp.combine_addition(one_result)
                    del dict_of_matrixs[ikey]
            count_get+=1
            no_msg_time = time.time()
        if time.time()-no_msg_time > time_before_resend:
            print(f'no message for {time_before_resend}s, try to check the black result')
            start_time_resend = time.time()            
            count_resend = 0
            count_num_for_resend = len(dict_of_matrixs)
            for key, value in dict_of_matrixs.items():
                one_pack_of_matrixs = value
                #print(one_pack_of_matrixs)
                message_id = sqs_function1.send_message(message = [one_pack_of_matrixs])
                count_resend+=1
                if time.time()-start_time_resend > time_before_print_process:
                    start_time = time.time()
                    print(f'        trying to resending...{count_resend}/{count_num_for_resend} ')
                print(f'        trying to resending...{count_resend}/{count_num_for_resend} ')
            if count_resend > 0:
                no_msg_time = time.time()
            else:
                break

        if time.time()-start_time > time_before_print_process:
            start_time = time.time()
            print(f'    trying to get results...{count_get}/{partition} ')

        if count_get == partition:
            break
    
    stop_time_getting_result = time.time()
    print(f'finish getting all result & combine...{count_get}/{partition}') 

    final_result = mp.get_result_addition()

    return final_result, start_time_getting_result, stop_time_getting_result

if __name__ == '__main__':
    
    master_addition(
        queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker', 
        region_name1 = 'us-east-1', 
        queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master', 
        region_name2 = 'us-east-1', 
        partition = 10, 
        m = 10, 
        n = 10, 
        randF=0, randT=10, 
        time_before_print_process=5, time_before_resend=15
        )


