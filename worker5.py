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
            status = evaluate_queue.evaluate_queue()
            print(status)
            start_time = time.time()


if __name__ == '__main__':
    
    try: 
        method = sys.argv[0]
        queue_url1 = sys.argv[1]
        region_name1 = sys.argv[2]
        queue_url2 = sys.argv[3]
        region_name2 = sys.argv[4]
        try:
            check_queue = sys.argv[5]
        except:
            check_queue = None
        
        worker(
            method = method,
            queue_url1 = queue_url1, 
            region_name1 = region_name1, 
            queue_url2 = queue_url2, 
            region_name2 = region_name2,
            check_queue = check_queue
            )
    except:
        worker(
            method = 'addtition',
            queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker', 
            region_name1 = 'us-east-1', 
            queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master', 
            region_name2 = 'us-east-1',
            check_queue = None
            )
