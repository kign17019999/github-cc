import numpy as np
import time
import random

"""
class definition
...
"""

class MatrixParallel:
    def __init__(self):
        self.result_addition = np.empty(0)
        self.result_multiplication = np.empty(0)
        
    
    def gen_matrix(self, rowSize, columnSize, randFrom, randTo):
        # Create a list of random integers
        matrix = random.sample(range(randFrom, randTo), rowSize * columnSize)        
        
        # Reshape the list into a 2D matrix
        matrix = np.reshape(matrix, (rowSize, columnSize))

        return matrix
    
    def decompose_for_addition(self, matrix1, matrix2, partition):
        # Split the input matrices into sub-matrices along the row axis
        sub_matrixs1 = np.array_split(matrix1, matrix1.shape[0], axis=0)
        sub_matrixs2 = np.array_split(matrix2, matrix2.shape[0], axis=0)

        result_row = matrix1.shape[0]
        result_col = matrix2.shape[1]
        self.result_addition = np.zeros((result_row, result_col))

        # Create a list of matrix pairs to be processed in parallel
        pack_of_matrixs = [
            ([index_row], [index_col], np.ascontiguousarray(sub_matrix1), np.ascontiguousarray(sub_matrix2))
            for index_row, (sub_matrix1, sub_matrix2) in enumerate(zip(sub_matrixs1, sub_matrixs2))
            for index_col in range(sub_matrix1.shape[1])
        ]


        dict_of_matrixs = {f"{index_row}-{index_col}": None for index_row, _, _, _ in pack_of_matrixs for index_col in range(sub_matrixs1.shape[1])}

        return pack_of_matrixs, dict_of_matrixs

    def addition(self, one_pack_of_matrixs):

        # Unpack the input matrix pairs
        index_row, index_col, a, b = one_pack_of_matrixs

        # Perform matrix addition
        result = np.add(a, b)
        
        # Construct the output list
        result_one_pack_of_matrixs = [index_row, index_col, result]

        return result_one_pack_of_matrixs

    def combine_addition(self, result_one_pack_of_matrixs):
        index_row = result_one_pack_of_matrixs[0][0]
        index_col = result_one_pack_of_matrixs[1][0]
        result_sub_matrix = np.array(result_one_pack_of_matrixs[2])
        
        num_rows_sub, num_cols_sub = result_sub_matrix.shape

        self.result_addition[index_row:index_row + num_rows_sub, index_col:index_col + num_cols_sub] = result_sub_matrix
        
        return 'this combine is done'


    def get_result_addition(self):
        return self.result_addition


    def decompose_for_multiplication(self, matrix1, matrix2, partition):
        sub_matrixs1 = np.vsplit(matrix1, matrix1.shape[0])
        sub_matrixs2 = np.hsplit(matrix2, matrix2.shape[1])
        
        result_row = matrix1.shape[0]
        result_col = matrix2.shape[1]
        self.result_multiplication = np.zeros((result_row, result_col))

        pack_of_matrixs = []
        dict_of_matrixs = {}
        
        index = 0

        if result_row*result_col < partition:
            min_in_each_parition  = partition//(result_row*result_col)
        else:
            min_in_each_parition = 1
        max_in_each_parition  = min_in_each_parition+1
        num_max_in_each_parition = partition%(result_row*result_col)
        
        for i in range(result_row):
            for j in range(result_col):
                if num_max_in_each_parition != 0:
                    sub_of_sub_matrixs1 = np.array_split(sub_matrixs1[i], max_in_each_parition, axis = 1)
                    sub_of_sub_matrixs2 = np.array_split(sub_matrixs2[j], max_in_each_parition, axis = 0)
                    len_sub_of_sub = max_in_each_parition
                    num_max_in_each_parition-=1
                else:
                    sub_of_sub_matrixs1 = np.array_split(sub_matrixs1[i], min_in_each_parition, axis = 1)
                    sub_of_sub_matrixs2 = np.array_split(sub_matrixs2[j], min_in_each_parition, axis = 0)   
                    len_sub_of_sub = min_in_each_parition    
                for sub_index in range(len_sub_of_sub):
                  a = sub_of_sub_matrixs1[sub_index].tolist()
                  b = sub_of_sub_matrixs2[sub_index].tolist()
                  one_pack_of_matrixs = [[index], [sub_index], a, b]
                  pack_of_matrixs.append(one_pack_of_matrixs)
                  dict_of_matrixs.update({f'{index}-{sub_index}':None})
                index+=1

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
        index = result_one_pack_of_matrixs[0]
        index_row = index[0]//self.result_multiplication.shape[1]
        index_col = index[0]%self.result_multiplication.shape[1]
        self.result_multiplication[index_row][index_col] +=result_one_pack_of_matrixs[2][0]
        
        return 'this combine is done'

    def get_result_multiplication(self):
        return self.result_multiplication