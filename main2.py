from sqsfunction import SQSFunction
from matrixparallel import MatrixParallel
import numpy as np

def main():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/183243280383/queue2'
    region_name = 'us-east-1'
    sqs_function = SQSFunction(queue_url, region_name)
    
    available_worker = 3
    partition = 4
    axis = 0
    m = 10
    n = 10
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
                'Worker': {
                    'DataType': 'String',
                    'StringValue': str(i%available_worker)
                }
            } 
        )  
    while True:
        # Receive the message with the message attributes
        message, message_attributes = sqs_function.receive_message()

        if message is not None:
            print(f'Message received: {message}')
            print(f'Message attributes: {message_attributes}')
        else:
            # Stop receiving messages if there are no more messages in the queue
            break

    
if __name__ == '__main__':
    main()