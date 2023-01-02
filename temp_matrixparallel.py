import numpy as np
import time

class MatrixParallel:
    def __init__(self):
        pass
    
    def gen_matrix(self, rowSize, columnSize, randFrom, randTo):
        # create random number in given size of array
        matrix = np.random.randint(randFrom, randTo, size = (rowSize, columnSize))
        
        return matrix
    
    def decompose_for_addition(self, matrix1, matrix2, partition, axis = 0):
        if axis != 0:
            matrix1 = matrix1.transpose()
            matrix2 = matrix2.transpose()
        
        sub_matrixs1 = np.array_split(matrix1, partition, axis = 0)
        sub_matrixs2 = np.array_split(matrix2, partition, axis = 0)
        axis_indices = np.arange(partition)
        
        list_of_sub_matrixs1 = [array.tolist() for array in sub_matrixs1]
        list_of_sub_matrixs2 = [array.tolist() for array in sub_matrixs2]
        list_of_axis_indices = axis_indices.tolist()
        pack_of_matrixs = [list_of_axis_indices, list_of_sub_matrixs1, list_of_sub_matrixs2]

        return pack_of_matrixs
    
    def addition(self, one_pack_of_matrixs):
        axis_indices = one_pack_of_matrixs[0]
        matrix1 = np.array(one_pack_of_matrixs[1])
        matrix2 = np.array(one_pack_of_matrixs[2])
        result = matrix1+matrix2
        result_one_pack_of_matrixs = []
        result_one_pack_of_matrixs.append(axis_indices)
        result_one_pack_of_matrixs.append(result.tolist())
        return result_one_pack_of_matrixs
    
    def combine_addition(self, list_of_results, axis = 0):
        dict_result = {}
        for i in range(len(list_of_results)):
            temp_dict = {list_of_results[i][0]:np.array(list_of_results[i][1])}
            dict_result.update(temp_dict)
        
        final_array = dict_result[0]
        for i in range(len(list_of_results)):
            if i==0:
                pass
            else:
                final_array = np.vstack((final_array,dict_result[i]))
        if axis == 1: final_array = final_array.transpose()
            
        return final_array
        
    def decompose_for_multiplication(self, matrix1, matrix2, partition):
        matrix1_submatrices = np.vsplit(matrix1, matrix1.shape[0])
        matrix2_submatrices = np.hsplit(matrix2, matrix2.shape[1])
        pack1 = []
        result_row = matrix1.shape[0]
        result_col = matrix2.shape[1]
        num = 0
        mod_r = result_row%partition
        min_in_part = result_row//partition
        max_in_part = min_in_part+1
        num_max_in_part = mod_r
        
        for i in range(result_row):
            for j in range(result_col):
                if max_in_part != 0:
                    matrix1_submatrices_temp = np.array_split(matrix1_submatrices[i], max_in_part, axis = 1)
                    matrix2_submatrices_temp = np.array_split(matrix2_submatrices[j], max_in_part, axis = 0)
                    k_temp = max_in_part
                    max_in_part-=1
                else:
                    matrix1_submatrices_temp = np.array_split(matrix1_submatrices[i], min_in_part, axis = 1)
                    matrix2_submatrices_temp = np.array_split(matrix2_submatrices[j], min_in_part, axis = 0)   
                    k_temp = min_in_part    
            for k in range(k_temp):
              tempL = [num, k, matrix1_submatrices_temp[k], matrix2_submatrices_temp[k]]
              a = matrix1_submatrices_temp[k].tolist()
              b = matrix2_submatrices_temp[k].tolist()
              tempL_vList = [[num], [k], a, b]
              #tempL_vList = [array.tolist() for array in tempL]
              pack1.append(tempL_vList)
              print(k)
            num+=1
            
        return pack1
    
    def multiplication(self, one_pack_of_matrixs):
        r = pack1[i][0]
        rr = pack1[i][1]
        a = np.array(pack1[i][2])
        b = np.array(pack1[i][3])
        result = np.dot(a,b)
        tempR = [r, rr, result]
        
        return tempR
    
    def combine_multiplication(self, list_of_results):
        final = np.zeros((result_row, result_col))
        for i in range(len(list_of_results)):
            index = list_of_results[i][0]
            index_row = index//result_col
            index_col = index%result_col
            final[index_row][index_col] += list_of_results[i][2][0]
            
        return final