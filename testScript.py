import master5mp as m5
import queue_delete_msg as qdm

#******************************************************************************

# design metrix and number of package
m1 = 100
n1 = 100
m2 = 100
n2 = 100
partition = 100

#config mode
method = 'addition'
#method = 'multiplication'
parallel = False

#******************************************************************************

m5.master(
    method = method,
    queue_url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker', 
    region_name1 = 'us-east-1', 
    queue_url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master', 
    region_name2 = 'us-east-1', 
    partition = partition, 
    m1 = m1, 
    n1 = n1, 
    m1 = m2, 
    n1 = n2, 
    randF=0, randT=10, 
    time_before_print_process=5, time_before_resend=15,
    parallel = parallel
)