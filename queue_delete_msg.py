from sqsfunction import SQSFunction
import numpy as np


def delete_msg(queue_url, region_name):
    
    queue_name = queue_url.rsplit('/', 1)[-1]

    print(f'trying delete msg in "{queue_name}"...')

    sqs_function = SQSFunction(queue_url, region_name)

    # Receive all messages in the queue
    while True:
        # Receive the message with the message attributes
        message = sqs_function.receive_message()

        if message is not None:
            #print(f'Message received: {message}')
            pass
        else:
            # Stop receiving messages if there are no more messages in the queue
            break

if __name__ == '__main__':
    delete_msg(queue_url='https://sqs.us-east-1.amazonaws.com/183243280383/queue2', region_name='us-east-1')
    delete_msg(queue_url='https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker', region_name='us-east-1')
    delete_msg(queue_url='https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master', region_name='us-east-1')