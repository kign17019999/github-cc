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
    
    # metrix operation
    mp = MatrixParallel()
    
    print('start receving & processing & send to master_queue...')
    i = 0
    while True:
        message = sqs_function1.receive_message()
        if message is not None:
            result = mp.addition(message)
            message_id = sqs_function2.send_message(message=result)
            i+=1
            print(f'{i}: message_id: {message_id}')


if __name__ == '__main__':
    main()
