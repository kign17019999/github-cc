import boto3
import pickle

class SQSFunction:
    def __init__(self, queue_url, region_name):
        self.sqs = boto3.client('sqs', region_name=region_name)
        self.queue_url = queue_url

    def send_message(self, message, message_attributes):
        # Serialize the message using pickle
        serialized_message = pickle.dumps(message)

        # Send the message with message attributes
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=serialized_message,
            MessageAttributes=message_attributes
        )

        return response['MessageId']

    def receive_message(self, message_attribute_names):
        # Receive the message with the message attributes
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            MessageAttributeNames=message_attribute_names
        )

        # Deserialize the message using pickle
        if 'Messages' in response:
            message = response['Messages'][0]
            serialized_message = message['Body']
            message = pickle.loads(serialized_message)
            return message, message['MessageAttributes']
        else:
            return None, None
