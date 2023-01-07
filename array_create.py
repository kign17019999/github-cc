import numpy as np
size = 1000

for i in range(100, size+1, 100):
    try:
        matrix = np.random.randint(0, 9, size = (i, i))
        print(f' {i} is OK')
    except Exception as e:
        print(f' {i} is not OK with following error')
        print(e)