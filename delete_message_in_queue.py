from sqsfunction import SQSFunction
import numpy as np

print('trying queue2 ...')
# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue2'
region_name = 'us-east-1'

sqs_function = SQSFunction(queue_url, region_name)

# Receive all messages in the queue
while True:
    # Receive the message with the message attributes
    message = sqs_function.receive_message()

    if message is not None:
        print(f'Message received: {message}')
    else:
        # Stop receiving messages if there are no more messages in the queue
        break
        
#******************************************************************************************************#      
print('trying queue_to_worker ...')        
# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
region_name = 'us-east-1'

sqs_function = SQSFunction(queue_url, region_name)

# Receive all messages in the queue
while True:
    # Receive the message with the message attributes
    message = sqs_function.receive_message()

    if message is not None:
        print(f'Message received: {message}')
    else:
        # Stop receiving messages if there are no more messages in the queue
        break

#******************************************************************************************************#
print('trying queue_to_master ...')         
# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
region_name = 'us-east-1'

sqs_function = SQSFunction(queue_url, region_name)

# Receive all messages in the queue
while True:
    # Receive the message with the message attributes
    message = sqs_function.receive_message()

    if message is not None:
        print(f'Message received: {message}')
    else:
        # Stop receiving messages if there are no more messages in the queue
        break
