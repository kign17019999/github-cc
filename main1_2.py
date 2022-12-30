from sqsfunction import SQSFunction
import numpy as np

# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue2'
region_name = 'us-east-1'

# Create an instance of the SQSFunction class
sqs_function = SQSFunction(queue_url, region_name)

data = np.array([1, 2, 3, 4, 6, 7])
data = data.tolist()

# Send a message w/ message attributes
message_id = sqs_function.send_message(data, {
    'Worker': {
        'StringValue': '1',
        'DataType': 'String'
        
    }
})

print(f'Message sent with ID: {message_id}')

# Receive the message w/ the message attributes
message, message_attributes = sqs_function.receive_message(attribute_name='Worker', attribute_value='1')

if message is not None:
    print(f'Message received: {message}')
    print(f'Message attributes: {message_attributes}')
else:
    print('No messages in the queue')
    
    
    
# Send a message w/ message attributes
message_id = sqs_function.send_message(data, {
    'Worker': {
        'StringValue': '11',
        'DataType': 'String'
        
    }
})

# Send a message w/ message attributes
message_id = sqs_function.send_message(data, {
    'Worker': {
        'StringValue': '12',
        'DataType': 'String'
        
    }
})

# Receive the message w/ the message attributes
message, message_attributes = sqs_function.receive_message_no_delete(attribute_name='Worker', attribute_value='11')

if message is not None:
    print(f'Message received: {message}')
    print(f'Message attributes: {message_attributes}')
else:
    print('No messages in the queue')
    
# Receive the message w/ the message attributes
message, message_attributes = sqs_function.receive_message_no_delete(attribute_name='Worker', attribute_value='12')

if message is not None:
    print(f'Message received: {message}')
    print(f'Message attributes: {message_attributes}')
else:
    print('No messages in the queue')
    
    
# Receive the message w/ the message attributes
message, message_attributes = sqs_function.receive_message_no_delete(attribute_name='Worker', attribute_value='11')

if message is not None:
    print(f'Message received: {message}')
    print(f'Message attributes: {message_attributes}')
else:
    print('No messages in the queue')
