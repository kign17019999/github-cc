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


    available_worker = 3
    partition = 5
    axis = 0
    m = 10
    n = 10
    randF = 0
    randT = 10

    # metrix operation
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m,n,randF,randT)
    mat2 = mp.gen_matrix(m,n,randF,randT)
    matlist = mp.decompose_for_addition(mat1, mat2, partition, axis = axis)

    print('start sending..')
    for i in range(partition):
        index = matlist[0][i]
        sub_mat1 = matlist[1][i]
        sub_mat2 = matlist[2][i]
        one_pack_of_matrixs = [index, sub_mat1, sub_mat2]
        message_id = sqs_function1.send_message(message = one_pack_of_matrixs)
        print(f'{i}: message_id: {message_id}')
    
    print('start receving & processing & send to master_queue')
    for i in range(partition):
        print(f'trying in worker {i%available_worker}')
        message = sqs_function1.receive_message()
        if message is not None:
            result = mp.addition(message)
            message_id = sqs_function2.send_message(message=result)
            print(f'{i}: message_id: {message_id}')


    print('start combinding...')
    all_result = []
    start_time = time.time()
    while len(all_result) != partition:
        message = sqs_function2.receive_message()
        if message is not None:
            all_result.append(message)
        time = time.time()
        if time.time()-start_time > 5:
            start_time = time.time()
            print(f'trying to reciving...{len(all_result)}/{partition} ')

    final_result = mp.combine_addition(list_of_results = all_result, axis = axis)
    print(final_result == mat1+mat2)


if __name__ == '__main__':
    main()
