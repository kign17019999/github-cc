from sqsfunction import SQSFunction
import numpy as np

# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue1'
region_name = 'us-east-1'

sqs_function = SQSFunction(queue_url, region_name)

# Receive all messages in the queue
while True:
    # Receive the message with the message attributes
    message, message_attributes = sqs_function.receive_message(['MessageType'])

    if message is not None:
        print(f'Message received: {message}')
        print(f'Message attributes: {message_attributes}')
    else:
        # Stop receiving messages if there are no more messages in the queue
        break
