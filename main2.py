from sqsfunction import SQSFunction
from matrixparallel import MatrixParallel
import numpy as np

def main():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue1'
    region_name = 'us-east-1'
    sqs_function = SQSFunction(queue_url, region_name)
    
    available_worker = 2
    partition = 2
    axis = 0
    m = 3
    n = 3
    randF = 0
    randT = 10
    
    # metrix operation
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m,n,randF,randT)
    mat2 = mp.gen_matrix(m,n,randF,randT)
    matlist = mp.decompose_for_addition(mat1, mat2, partition, axis = axis)
    
    for i in range(partition):
        index = matlist[0][i]  
        sub_mat1 = matlist[1][i] 
        sub_mat2 = matlist[2][i]
        one_pack_of_matrixs = [index, sub_mat1, sub_mat2]
        message_id = sqs_function.send_message(
            message = one_pack_of_matrixs,
            message_attributes = {
                str(i%available_worker): {
                    'DataType': 'String',
                    'StringValue': str(i%available_worker)
                }
            } 
        )
    ii = 0    
    while True:
        # Receive the message with the message attributes
        message, message_attributes = sqs_function.receive_message([str(ii%available_worker)])

        if message is not None:
            print(f'Message received: {message}')
            print(f'Message attributes: {message_attributes}')
        else:
            # Stop receiving messages if there are no more messages in the queue
            break
        
        ii+=1

    
if __name__ == '__main__':
    main()