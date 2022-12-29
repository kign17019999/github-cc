import boto3
import json

class SQSFunction:
    def __init__(self, queue_url, region_name):
        self.sqs = boto3.client('sqs', region_name=region_name)
        self.queue_url = queue_url

    def send_messages(self, messages):
        # Create a list to store the message bodies
        message_bodies = []
        
        # Iterate over the messages and add their bodies to the list
        for message in messages:
            # Serialize the message using json
            serialized_message = json.dumps(message)
            message_bodies.append(serialized_message)
        
        # Send the batch of messages all at once
        response = self.sqs.send_message_batch(
            QueueUrl=self.queue_url,
            Entries=[{'Id': str(i), 'MessageBody': message} for i, message in enumerate(message_bodies)]
        )
        
        # Return the list of message IDs
        return [response['Successful'][i]['MessageId'] for i in range(len(response['Successful']))]

    def receive_message(self, message_attribute_names):
        # Receive a message from the queue
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            MessageAttributeNames=message_attribute_names
        )

        # Check if a message was received
        if 'Messages' in response:
            # Get the message body, attributes, and receipt handle
            message_body = response['Messages'][0]['Body']
            message_attributes = response['Messages'][0]['MessageAttributes']
            receipt_handle = response['Messages'][0]['ReceiptHandle']

            # Deserialize the message using json
            message = json.loads(message_body)

            # Delete the message from the queue
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )

            # Return the message and attributes
            return message, message_attributes
        else:
            print('No messages in the queue')
            return None, None
