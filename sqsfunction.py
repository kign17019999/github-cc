import boto3
import json

class SQSFunction:
    def __init__(self, queue_url, region_name):
        self.sqs = boto3.client('sqs', region_name=region_name)
        self.queue_url = queue_url

    def send_message(self, message, message_attributes=None):
        # Serialize the message using json
        serialized_message = json.dumps(message)

        # Send the message with message attributes (if specified)
        if message_attributes:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=serialized_message,
                MessageAttributes=message_attributes
            )
        else:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=serialized_message
            )

        return response['MessageId']

    def receive_message(self, attribute_name=None, attribute_value=None):
        # Receive a message from the queue with message attributes (if specified)
        if attribute_name:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                MessageAttributeNames=[attribute_name]
            )
        else:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1
            )        
        
        # Check if a message was received
        if 'Messages' in response:
            if 'MessageAttributes' in response['Messages'][0]:
                if attribute_value:
                    message_attribute_value = response['Messages'][0]['MessageAttributes'][attribute_name]['StringValue']
                    if message_attribute_value != attribute_value:
                        print('No messages in the queue')
                        return None, None
            # Get the message body, attributes, and receipt handle
            message_body = response['Messages'][0]['Body']
            if attribute_name:
                message_attributes = response['Messages'][0]['MessageAttributes']
            else:
                message_attributes = None
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



    def receive_message_no_delete(self, attribute_name=None, attribute_value=None):
        # Receive a message from the queue with message attributes (if specified)
        if attribute_name:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                MessageAttributeNames=[attribute_name]
            )
        else:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1
            )        
        
        # Check if a message was received
        if 'Messages' in response:
            if 'MessageAttributes' in response['Messages'][0]:
                if attribute_value:
                    message_attribute_value = response['Messages'][0]['MessageAttributes'][attribute_name]['StringValue']
                    if message_attribute_value != attribute_value:
                        print('No messages in the queue')
                        return None, None
            # Get the message body, attributes, and receipt handle
            message_body = response['Messages'][0]['Body']
            if attribute_name:
                message_attributes = response['Messages'][0]['MessageAttributes']
            else:
                message_attributes = None
            receipt_handle = response['Messages'][0]['ReceiptHandle']

            # Deserialize the message using json
            message = json.loads(message_body)

            # Return the message and attributes
            return message, message_attributes
        else:
            print('No messages in the queue')
            return None, None
            
            
    def delete_message_in_queue(self, receipt_handle):
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
        