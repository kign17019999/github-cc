from sqsfunction import SQSFunction
from matrixparallel_v2 import MatrixParallel
import numpy as np
import time

def main():
    
    queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
    region_name1 = 'us-east-1'
    sqs_function1 = SQSFunction(queue_url1, region_name1)
    
    queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
    region_name2 = 'us-east-1'
    sqs_function2 = SQSFunction(queue_url2, region_name2)

    print('acting as a master')

    partition = 10
    axis = 0
    m = 10
    n = 10
    randF = 0
    randT = 10

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


    # metrix operation
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m,n,randF,randT)
    mat2 = mp.gen_matrix(m,n,randF,randT)
    pack_of_matrixs, dict_of_matrixs = mp.decompose_for_addition(mat1, mat2, partition)
    
    start_time0 = time.time()
    
    start_time = time.time()
    print('start sending..')
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
        if time.time()-start_time > 15:
            start_time = time.time()
            print(f'trying to sending...{i}/{partition} ')
    
    print(f'finishing sending...{partition}/{partition} ')
    
    start_time_getting_result = time.time()
    print('start getting result & combine...')
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
        if time.time()-no_msg_time > 15:
            print(f'no message for 15s, try to check the black result')            
            count_resend = 0
            for key, value in dict_of_matrixs.items():
                if value is not None:
                    one_pack_of_matrixs = value
                    print(one_pack_of_matrixs)
                    message_id = sqs_function1.send_message(message = [one_pack_of_matrixs])
                    count_resend+=1
            if count_resend > 0:
                no_msg_time = time.time()
            else:
                break

        if time.time()-start_time > 5:
            start_time = time.time()
            print(f'trying to get results...{count_get}/{partition} ')

        if count_get == partition:
            break
    
    print(f'finish getting all result & combine...{count_get}/{partition}')
    print(f'time getting all result: {time.time()-start_time_getting_result}')       
    
    final_result = mp.get_result_addition()

    totle_dist_time = time.time()-start_time0
    
    start_time1 = time.time()
    result_with_local = mat1+mat2
    totle_local_time = time.time()-start_time1
    
    
    print(final_result == result_with_local)
    
    print(f'total time dist : {totle_dist_time}')
    print(f'total time local: {totle_local_time}')
    

if __name__ == '__main__':
    main()
