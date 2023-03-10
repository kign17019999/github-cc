import numpy as np
import time
import itertools

"""
class definition
...
"""

class MatrixParallel:
    def __init__(self):
        self.result_addition = np.empty(0)
        self.result_multiplication = np.empty(0)

        self.decomp_count_add = 0
        self.decomp_count_mul = 0
        
    
    def gen_matrix(self, rowSize, columnSize, randFrom, randTo):
        # create random number in given size of array 
        # and the range of random number which will be a value in each element
        #matrix = np.random.randint(randFrom, randTo, size = (rowSize, columnSize))
        matrix = np.random.randint(randFrom, randTo, size = (rowSize, columnSize))
        
        return matrix
    
    def decompose_for_addition(self, matrix1, matrix2, partition, time_before_print_process):
        self.decomp_count_add = 0

        result_row = matrix1.shape[0]
        result_col = matrix2.shape[1]
        self.result_addition = np.zeros((result_row, result_col))

        pack_of_matrixs = []
        dict_of_matrixs = {}

        one_pack_of_matrixs = [[],[],[],[]]
        if result_row < partition:
            min_in_each_parition  = partition//result_row
            num_max_in_each_parition = partition%result_row
            total_decompose_num = partition
        else:
            min_in_each_parition = 1
            num_max_in_each_parition = 0
            total_decompose_num = result_row
        
        max_in_each_parition  = min_in_each_parition+1
        
        start_time = time.time()
        for index_row in range(result_row):
            sub_matrix1 = matrix1[index_row, :].reshape(1, -1)
            sub_matrix2 = matrix2[index_row, :].reshape(1, -1)
            if num_max_in_each_parition != 0:
                sub_of_sub_matrixs1 = np.array_split(sub_matrix1, max_in_each_parition, axis = 1)
                sub_of_sub_matrixs2 = np.array_split(sub_matrix2, max_in_each_parition, axis = 1)
                len_sub_of_sub = max_in_each_parition
                num_max_in_each_parition-=1
            else:

                sub_of_sub_matrixs1 = np.array_split(sub_matrix1, min_in_each_parition, axis = 1)
                sub_of_sub_matrixs2 = np.array_split(sub_matrix2, min_in_each_parition, axis = 1)   
                len_sub_of_sub = min_in_each_parition
            index_col = 0 #shape[1] of previous is a starting next element index
            one_pack_of_matrixs[0] = [index_row]
            '''
            for sub_index, (a, b) in enumerate(zip(sub_of_sub_matrixs1, sub_of_sub_matrixs2)):
                a = a.tolist()
                b = b.tolist()
                one_pack_of_matrixs[1] = [index_col]
                one_pack_of_matrixs[2] = a
                one_pack_of_matrixs[3] = b
                pack_of_matrixs.append(list(one_pack_of_matrixs))
                dict_of_matrixs.update({f'{index_row}-{index_col}': list(one_pack_of_matrixs)})
                index_col += np.array(a).shape[1]
                self.decomp_count_add +=1
                if time.time()-start_time > time_before_print_process:
                    start_time = time.time()
                    print(f'    trying to decompose into {self.decomp_count_add}/{total_decompose_num} parts')

            '''
            for sub_index in range(len_sub_of_sub):
                a = sub_of_sub_matrixs1[sub_index].tolist()
                b = sub_of_sub_matrixs2[sub_index].tolist()
                one_pack_of_matrixs[1] = [index_col]
                one_pack_of_matrixs[2] = a
                one_pack_of_matrixs[3] = b
                pack_of_matrixs.append(list(one_pack_of_matrixs))
                dict_of_matrixs.update({f'{index_row}-{index_col}':list(one_pack_of_matrixs)})
                index_col += np.array(a).shape[1]
                self.decomp_count_add +=1
                if time.time()-start_time > time_before_print_process:
                    start_time = time.time()
                    print(f'    trying to decompose into {self.decomp_count_add}/{total_decompose_num} parts')
        print(f'    finishing decompose into {self.decomp_count_add}/{total_decompose_num} parts')
        return pack_of_matrixs, dict_of_matrixs

    def addition(self, one_pack_of_matrixs):

        index_row = one_pack_of_matrixs[0]
        index_col = one_pack_of_matrixs[1]

        a = np.array(one_pack_of_matrixs[2])
        b = np.array(one_pack_of_matrixs[3])
        result = a+b
        result_one_pack_of_matrixs = []
        result_one_pack_of_matrixs.append(index_row)
        result_one_pack_of_matrixs.append(index_col)
        result_one_pack_of_matrixs.append(result.tolist())

        return result_one_pack_of_matrixs

    def combine_addition(self, result_one_pack_of_matrixs):
        comb_state = False
        try:
            index_row = result_one_pack_of_matrixs[0][0]
            index_col = result_one_pack_of_matrixs[1][0]
            result_sub_matrix = np.array(result_one_pack_of_matrixs[2])
            
            num_rows_sub, num_cols_sub = result_sub_matrix.shape

            self.result_addition[index_row:index_row + num_rows_sub, index_col:index_col + num_cols_sub] = result_sub_matrix
            comb_state = True
        except:
            pass
        return comb_state


    def get_result_addition(self):
        return self.result_addition


    def decompose_for_multiplication(self, matrix1, matrix2, partition, time_before_print_process):

        self.decomp_count_mul = 0

        #sub_matrixs1 = np.vsplit(matrix1, matrix1.shape[0])
        #sub_matrixs2 = np.hsplit(matrix2, matrix2.shape[1])
        
        result_row = matrix1.shape[0]
        result_col = matrix2.shape[1]
        self.result_multiplication = np.zeros((result_row, result_col))

        pack_of_matrixs = []
        dict_of_matrixs = {}
        
        index = 0
        one_pack_of_matrixs = [[],[],[],[]]
        if result_row*result_col < partition:
            min_in_each_parition  = partition//(result_row*result_col)
            num_max_in_each_parition = partition%(result_row*result_col)
            total_decompose_num = partition

        else:
            min_in_each_parition = 1
            num_max_in_each_parition = 0
            total_decompose_num = result_row*result_col
        max_in_each_parition  = min_in_each_parition+1
        
        '''
        start_time = time.time()
        for i in range(result_row):
            for j in range(result_col):
                sub_matrix1 = matrix1[i, :].reshape(1, -1)
                sub_matrix2 = matrix2[:, j].reshape(1, -1)
                if num_max_in_each_parition != 0:
                    sub_of_sub_matrixs1 = np.array_split(sub_matrix1, max_in_each_parition, axis = 1)
                    sub_of_sub_matrixs2 = np.array_split(sub_matrix2, max_in_each_parition, axis = 0)
                    len_sub_of_sub = max_in_each_parition
                    num_max_in_each_parition-=1
                else:
                    sub_of_sub_matrixs1 = np.array_split(sub_matrix1, min_in_each_parition, axis = 1)
                    sub_of_sub_matrixs2 = np.array_split(sub_matrix2, min_in_each_parition, axis = 0)   
                    len_sub_of_sub = min_in_each_parition    
                for sub_index in range(len_sub_of_sub):
                    a = sub_of_sub_matrixs1[sub_index].tolist()
                    b = sub_of_sub_matrixs2[sub_index].tolist()
                    one_pack_of_matrixs[0] = [index]
                    one_pack_of_matrixs[1] = [sub_index]
                    one_pack_of_matrixs[2] = a
                    one_pack_of_matrixs[3] = b
                    pack_of_matrixs.append(list(one_pack_of_matrixs))
                    dict_of_matrixs.update({f'{index}-{sub_index}':list(one_pack_of_matrixs)})
                    self.decomp_count_mul +=1
                    if time.time()-start_time > time_before_print_process:
                        start_time = time.time()
                        print(f'    trying to decompose into {self.decomp_count_mul}/{total_decompose_num} parts')                    
                index+=1
        '''
        start_time = time.time()
        for i, j in itertools.product(range(result_row), range(result_col)):
            sub_matrix1 = matrix1[i, :].reshape(1, -1)
            sub_matrix2 = matrix2[:, j].reshape(-1, 1)
            if num_max_in_each_parition != 0:
                sub_of_sub_matrixs1 = np.array_split(sub_matrix1, max_in_each_parition, axis = 1)
                sub_of_sub_matrixs2 = np.array_split(sub_matrix2, max_in_each_parition, axis = 0)
                len_sub_of_sub = max_in_each_parition
                num_max_in_each_parition-=1
            else:
                sub_of_sub_matrixs1 = np.array_split(sub_matrix1, min_in_each_parition, axis = 1)
                sub_of_sub_matrixs2 = np.array_split(sub_matrix2, min_in_each_parition, axis = 0)   
                len_sub_of_sub = min_in_each_parition    
            for sub_index in range(len_sub_of_sub):
                a = sub_of_sub_matrixs1[sub_index].tolist()
                b = sub_of_sub_matrixs2[sub_index].tolist()
                one_pack_of_matrixs[0] = [index]
                one_pack_of_matrixs[1] = [sub_index]
                one_pack_of_matrixs[2] = a
                one_pack_of_matrixs[3] = b
                pack_of_matrixs.append(list(one_pack_of_matrixs))
                dict_of_matrixs.update({f'{index}-{sub_index}':list(one_pack_of_matrixs)})
                self.decomp_count_mul +=1
                if time.time()-start_time > time_before_print_process:
                    start_time = time.time()
                    print(f'    trying to decompose into {self.decomp_count_mul}/{total_decompose_num} parts')                    
            index+=1
        print(f'    finishing decompose into {self.decomp_count_mul}/{total_decompose_num} parts')
        return pack_of_matrixs, dict_of_matrixs
    
    def multiplication(self, one_pack_of_matrixs):

        index = one_pack_of_matrixs[0]
        sub_index = one_pack_of_matrixs[1]
        a = np.array(one_pack_of_matrixs[2])
        b = np.array(one_pack_of_matrixs[3])
        result = np.dot(a,b)
        result_one_pack_of_matrixs = []
        result_one_pack_of_matrixs.append(index)
        result_one_pack_of_matrixs.append(sub_index)
        result_one_pack_of_matrixs.append(result.tolist())
        
        return result_one_pack_of_matrixs
    
    def combine_multiplication(self, result_one_pack_of_matrixs):
        comb_state = False
        try:
            index = result_one_pack_of_matrixs[0]
            index_row = index[0]//self.result_multiplication.shape[1]
            index_col = index[0]%self.result_multiplication.shape[1]
            self.result_multiplication[index_row][index_col] +=result_one_pack_of_matrixs[2][0]
            comb_state = True
        except:
            pass  
        return comb_state

    def get_result_multiplication(self):
        return self.result_multiplication