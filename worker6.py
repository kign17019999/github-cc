from sqsfunction import SQSFunction
from matrixparallel_v2 import MatrixParallel
import evaluate_queue
import numpy as np
import sys
import time

time_before_evaluate_queue = 10

def worker(method, queue_url1, region_name1, queue_url2, region_name2, check_queue = None):
    
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
        if time.time() - start_time > time_before_evaluate_queue:
            evaluate_queue.evaluate_queue('worker6.py', method, queue_url1, region_name1, queue_url2, region_name2)
            start_time = time.time()


if __name__ == '__main__':
    
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
