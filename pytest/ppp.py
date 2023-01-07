import master5mp as m5
import queue_delete_msg as qdm
import result_log as rl
from boto3function import Boto3Function
import time

queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
region_name1 = 'us-east-1'
queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
region_name2 = 'us-east-1' 

b3f = Boto3Function(region_name1)

b3f.stop_worker(
    target_instance_id = 'i-055336f9cd0657c5c', 
    file_name = 'worker6.py', 
    method = 'addition', 
    queue_url1 = queue_url1, 
    region_name1 = region_name1, 
    queue_url2 = queue_url2, 
    region_name2 = region_name2, 
    check_queue = None
    )