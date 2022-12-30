from sqsfunction import SQSFunction
import numpy as np

# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue2'
region_name = 'us-east-1'

# Create an instance of the SQSFunction class
sqs_function = SQSFunction(queue_url, region_name)

# Receive the message w/ the message attributes
message, message_attributes = sqs_function.receive_message_no_delete(attribute_name='Worker', attribute_value='11')

if message is not None:
    print(f'Message received: {message}')
    print(f'Message attributes: {message_attributes}')
else:
    print('No messages in the queue')