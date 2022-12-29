# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue1'

# Create an instance of the SQSFunction class
sqs_function = SQSFunction(queue_url)

# Send a message with message attributes
message_id = sqs_function.send_message('Hello, World!', {
    'MessageType': {
        'DataType': 'String',
        'StringValue': 'Greeting'
    }
})

print(f'Message sent with ID: {message_id}')

# Receive the message with the message attributes
message, message_attributes = sqs_function.receive_message(['MessageType'])

if message is not None:
    print(f'Message received: {message}')
    print(f'Message attributes: {message_attributes}')
else:
    print('No messages in the queue')
