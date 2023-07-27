import numpy as np
from array import array

dataset = np.loadtxt("data.csv",delimiter=",", dtype=str)
da = []
for i in dataset :
    da.append(np.array(i))
print(da)
print(da[0])