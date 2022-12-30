import numpy as np

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
        
    def decompose_for_multiplication():
        pass
    
    def multiplication(self, metrix1, metrix2):
        pass
    
    def combine_multiplication(self, list_metrixs):
        pass