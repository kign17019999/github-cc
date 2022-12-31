from sqsfunction import SQSFunction
from matrixparallel import MatrixParallel
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

    partition = 500
    axis = 0
    m = 2000
    n = 2000
    randF = 0
    randT = 10

    # metrix operation
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m,n,randF,randT)
    mat2 = mp.gen_matrix(m,n,randF,randT)
    matlist = mp.decompose_for_addition(mat1, mat2, partition, axis = axis)
    
    start_time0 = time.time()
    
    start_time = time.time()
    print('start sending..')
    for i in range(partition):
        index = matlist[0][i]
        sub_mat1 = matlist[1][i]
        sub_mat2 = matlist[2][i]
        one_pack_of_matrixs = [index, sub_mat1, sub_mat2]
        message_id = sqs_function1.send_message(message = one_pack_of_matrixs)
        #print(f'{i}: message_id: {message_id}')
        if time.time()-start_time > 5:
            start_time = time.time()
            print(f'trying to sending...{i}/{partition} ')
    print(f'finishing sending...{partition}/{partition} ')
    
    print('start getting result...')
    all_result = []
    start_time = time.time()
    while len(all_result) != partition:
        message = sqs_function2.receive_message()
        if message is not None:
            all_result.append(message)
        if time.time()-start_time > 5:
            start_time = time.time()
            print(f'trying to get results...{len(all_result)}/{partition} ')
    
    print(f'time after getting all result: {time.time()-start_time0}')       
    print(f'trying to combinding...{partition}/{partition} ')

    final_result = mp.combine_addition(list_of_results = all_result, axis = axis)
    
    totle_dist_time = time.time()-start_time0
    
    start_time1 = time.time()
    result_with_local = mat1+mat2
    totle_local_time = time.time()-start_time1
    
    
    print(final_result == result_with_local)
    
    print(f'total time dist : {totle_dist_time}')
    print(f'total time local: {totle_local_time}')


if __name__ == '__main__':
    main()
