from matrixparallel_v2 import MatrixParallel
from matrixparallel_v2_temp import MatrixParallel as mpold
import numpy as np
import time

partition=10
#partition=5
m1=10
n1=m1
m2=m1
n2=m1
randF=0
randT=9
time_before_print_process = 10

mp = MatrixParallel()
mp2 = mpold()
print("--------------------")
print('start rand mat')
start_time0 = time.time()
mat1 = mp.gen_matrix(m1,n1,randF,randT)
mat2 = mp.gen_matrix(m2,n2,randF,randT)
finish0 = time.time() - start_time0
print('finishrand mat')
print(finish0)
print("--------------------")

#mat1 = np.array([[1,1,1],[2,2,2],[3,3,3]])
#mat2 = np.array([[4,4,4],[5,5,5],[6,6,6]])

start_time1 = time.time()
pack_of_matrixs1, dict_of_matrixs = mp.decompose_for_addition(mat1, mat2, partition, time_before_print_process)
finish1 = time.time() - start_time1 

start_time2 = time.time()
#pack_of_matrixs2, dict_of_matrixs = mp2.decompose_for_addition(mat1, mat2, partition, time_before_print_process)
finish2 = time.time() - start_time2

#print(pack_of_matrixs1 == pack_of_matrixs2)
#print(pack_of_matrixs1)
#print(pack_of_matrixs2)

print(finish1)
print(finish2)
print("--------------------")
start_time3 = time.time()
pack_of_matrixs3, dict_of_matrixs = mp.decompose_for_multiplication(mat1, mat2, partition, time_before_print_process)
finish3 = time.time() - start_time3 

start_time4 = time.time()
pack_of_matrixs4, dict_of_matrixs = mp2.decompose_for_multiplication(mat1, mat2, partition, time_before_print_process)
finish4 = time.time() - start_time4

print(pack_of_matrixs3 == pack_of_matrixs4)
print(finish3)
print(finish4)

print(pack_of_matrixs3[0])
print(pack_of_matrixs4[0])