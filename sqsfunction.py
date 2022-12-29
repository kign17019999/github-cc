import boto3
import pickle

class SQSFunction:
    def __init__(self, queue_url, region_name):
        self.sqs = boto3.client('sqs', region_name=region_name)
        self.queue_url = queue_url

    def send_message(self, message, message_attributes):
        # Serialize the message using pickle
        serialized_message = pickle.dumps(message)
        
        # Convert the serialized message to a string
        message_body = serialized_message.encode('utf-8')

        # Send the message with message attributes
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )

        return response['MessageId']

    def receive(self, message_attribute_names):
        # Receive a message from the queue
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            MessageAttributeNames=message_attribute_names
        )

        # Check if a message was received
        if 'Messages' in response:
            # Get the message body
            message_body = response['Messages'][0]['Body']

            # Deserialize the message using pickle
            message = pickle.loads(message_body.decode('utf-8'))

            # Print the message
            print(f'Message received: {message}')
        else:
            print('No messages in the queue')
            