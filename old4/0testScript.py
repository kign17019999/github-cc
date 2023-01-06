import master5mp as m5
import queue_delete_msg as qdm
import result_log as rl
from boto3function import Boto3Function
import time

def main():
    #******************************************************************************

    # design metrix and number of package
    m1 = 5
    n1 = 5
    m2 = 5
    n2 = 5
    partition = (m1*n2)//1

    # config mode
    method = 'addition'
    #method = 'multiplication'
    parallel = False


    # config URL
    queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
    region_name1 = 'us-east-1'
    queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
    region_name2 = 'us-east-1' 


    result = m5.master(
        method = method,
        queue_url1 = queue_url1, 
        region_name1 = region_name1, 
        queue_url2 = queue_url2, 
        region_name2 = region_name2, 
        partition = partition, 
        m1 = m1, 
        n1 = n1, 
        m2 = m2, 
        n2 = n2, 
        randF=0, randT=10, 
        time_before_print_process=5, time_before_resend=15,
        parallel = parallel
    )

    rl.add_or_create_log(
        fileName='system_mp_log.csv',
        fileDir='/home/ec2-user/github-cc/',
        dict_data=result
    )


if __name__ == '__main__':
    main()