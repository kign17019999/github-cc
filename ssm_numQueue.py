import boto3

# Connect to the SQS service
sqs = boto3.client('sqs', region_name = 'us-east-1')

# Set the queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'

# Use the get_queue_attributes method to retrieve the number of messages in the queue
response = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['ApproximateNumberOfMessages']
)

# Get the number of messages from the response
num_messages = int(response['Attributes']['ApproximateNumberOfMessages'])

# Print the number of messages
print(f'Number of messages: {num_messages}')
