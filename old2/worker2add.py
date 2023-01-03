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
    
    # metrix operation
    mp = MatrixParallel()
    
    print('acting as a worker')
    print('start receving & processing & send to master_queue...')
    count = 0
    while True:
        message = sqs_function1.receive_message()
        if message is not None:
            num_in_msg = len(message)
            results = []
            for j in range(num_in_msg):
                one_result = mp.addition(message[j])
                results.append(one_result)
            message_id = sqs_function2.send_message(message=results)
            count+=1
            print(f'    {count}: Done process & Sent result with msg_id: {message_id}')


if __name__ == '__main__':
    main()
