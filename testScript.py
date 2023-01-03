import master3add as m3a
import master3mul as m3m
import queue_delete_msg as qdm

#******************************************************************************

#for addition
partitionA = 100
m = 100
n = 100

#for multiplication
partitionM = 100
m1 = 100
n1 = 100
m2 = 100
n2 = 100

#config mode
wantAdd = True
wantMul = False

#******************************************************************************

url1 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_worker'
reg1 = 'us-east-1', 
url2 = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue_to_master'
reg2 = 'us-east-1', 

randFr = 0
reanTo = 100
timeP = 5
timeR = 15

if wantAdd == True:
    m3a.master_addition(
        queue_url1 = url1, region_name1 = reg1, queue_url2 = url2, region_name2 = reg2, 
        randF=randFr, randT=reanTo, time_before_print_process=timeP, time_before_resend=timeR,
        partition = partitionA, 
        m = m, 
        n = n
        )
if wantMul == True:
    m3m.master_multiplication(
        queue_url1 = url1, region_name1 = reg1, queue_url2 = url2, region_name2 = reg2, 
        randF=randFr, randT=reanTo, time_before_print_process=timeP, time_before_resend=timeR,
        partition = partitionM, 
        m1 = m1, 
        n1 = n1,
        m2 = m2, 
        n2 = n2
        )