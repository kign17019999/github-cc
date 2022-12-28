import boto3

# Create an SQS client
sqs = boto3.client('sqs')

# Set the URL of the queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'

# Send a message to the queue
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='Hello, world!'
)

# Print the message ID
print(response['MessageId'])