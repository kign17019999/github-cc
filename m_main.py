from metrixparallel import MetrixParallel
import masterworker import MasterWorker

def main():
    connections = [("localhost", 10100), ("localhost", 10101), ("localhost", 10102)]
    master = MasterWorker(connections)
    for i in range(len(master.sockets)):
        master.accept_connections(i)

    master.display_connections()
    
    import pickle

    # config
    available_worker = master.display_connections()
    print(f'available worker: {available_worker}')

    partition = 300
    axis = 0
    header_byte = 100
    length = 1024
    m = 1000
    n = 1000
    randF = 0
    randT = 1000

    # metrix operation
    mp = MatrixParallel()
    mat1 = mp.gen_matrix(m,n,randF,randT)
    mat2 = mp.gen_matrix(m,n,randF,randT)
    matlist = mp.decompose_for_addition(mat1, mat2, partition, axis = axis)
    #print(f'len matlist: {len(matlist)}')

    # send data to worker
    num_pack_for_master1 = partition//available_worker
    num_pack_for_master2 = partition - num_pack_for_master1
    #print(f'numpack1: {num_pack_for_master1}')
    #print(f'numpack2: {num_pack_for_master2}')

    for i in range(len(matlist)):
        #print(f'sendto {i%available_worker} with {matlist[i]}')
        message = pickle.dumps(matlist[i])    
        master.send_withHeader(message=message, header_byte=header_byte, connection_index=i%available_worker)

    data = []

    while len(data) != partition:
        for i in range(available_worker):
            date_from_worker = master.get_withHeader(header_byte=header_byte, length=length, connection_index=i)
            if date_from_worker != b"":
                #print(f'data from worker {i} : {date_from_worker}')
                date_pickle_from_worker = pickle.loads(date_from_worker)
                data.append(date_pickle_from_worker)
                #print(f'data from worker {i} : {date_pickle_from_worker}')
    result = mp.combine_addition(list_of_results = data, axis = axis)
    print(result == mat1+mat2)
    
    master.close_all()
    
if __name__ =="__main__":
    main()