from metrixparallel import MetrixParallel
import masterworker import MasterWorker

def main():
    connections = [("localhost", 10101)]
    worker = MasterWorker(connections, master = False)
    worker.display_connections()
    
    def process_metrix():
        header_byte = 100
        length = 1024
        data = []
        outcome = []

        while True:
            temp_data = worker.get_withHeader(header_byte=header_byte, length=length, connection_index=0)
            if temp_data == b"":
                if len(data) == 0:
                    continue
                else:
                    break
            temp_data_pickle = pickle.loads(temp_data)
            #print(f'temp_data_pickle={temp_data_pickle}') 
            data.append(pickle.loads(temp_data))

        #print(f'data={len(data)}') 
        #print(f'outcome={len(outcome)}')

        mp = MatrixParallel()
        iteration_number = len(data)
        for i in range(iteration_number):
            temp_add_result = mp.addition(data[0])
            #print(f'temp_add_result={len(temp_add_result)}') 
            outcome.append(temp_add_result)
            del data[0]

        iteration_number = len(outcome)
        for i in range(iteration_number):
            message = pickle.dumps(outcome[0])
            #print(f'message={len(message)}') 
            worker.send_withHeader(message=message, header_byte=header_byte, connection_index=0)
            del outcome[0]    

        #print(f'data={len(data)}')    
        #print(f'outcome={len(outcome)}')
        
    import pickle

    process_metrix()
    
    worker.close_all()
        
if __name__ == '__main__':
    main()