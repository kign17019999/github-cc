import boto3

# Create an SQS client
sqs = boto3.client('sqs')

# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue1'

# Send a message to the queue
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='Hello, world!'
)

# Print the message ID
print(response['MessageId'])