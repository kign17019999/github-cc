import numpy as np

class MatrixParallel:
    def __init__(self):
        pass
    
    def gen_matrix(self, rowSize, columnSize, randFrom, randTo):
        # create random number in given size of array
        metrix = np.random.randint(randFrom, randTo, size = (rowSize, columnSize))
        
        return metrix
    
    def decompose_for_addition(self, metrix1, metrix2, partition, axis = 0):
        if axis != 0:
            metrix1 = metrix1.transpose()
            metrix2 = metrix2.transpose()
        
        sub_metrixs1 = np.array_split(metrix1, partition, axis = 0)
        sub_metrixs2 = np.array_split(metrix2, partition, axis = 0)
        axis_indices = np.arange(partition)
        #pack_of_arrays = np.column_stack((axis_indices, sub_metrixs1, sub_metrixs2))
        ss = list(zip(axis_indices, sub_metrixs1, sub_metrixs2))
        pack_of_arrays = np.array(ss, dtype=object)

        return pack_of_arrays
    
    def addition(self, one_pack_of_array):
        axis_indices = one_pack_of_array[0]
        matrix1 = one_pack_of_array[1]
        matrix2 = one_pack_of_array[2]
        result = matrix1+matrix2
        result_one_pack_of_array = []
        result_one_pack_of_array.append(axis_indices)
        result_one_pack_of_array.append(result)
        return result_one_pack_of_array
    
    def combine_addition(self, list_of_results, axis = 0):
        dict_result = {}
        for i in range(len(list_of_results)):
            temp_dict = {list_of_results[i][0]:list_of_results[i][1]}
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