import boto3

# Create an SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# Send a message to the queue
response = sqs.send_message(
    QueueUrl='"https://sqs.us-east-1.amazonaws.com/183243280383/queue1",
    MessageBody='Hello, World!'
)

# Print the message ID
print(response['MessageId'])

# Receive a message from the queue
response = sqs.receive_message(
    QueueUrl='"https://sqs.us-east-1.amazonaws.com/183243280383/queue1",
    MaxNumberOfMessages=1
)

# Print the message body
print(response['Messages'][0]['Body'])


I


