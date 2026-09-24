import numpy as np

a = np.arange(50000).reshape(1000, 50)


b1 = a[10:20] # view
b2 = a[::-2] # view
b3 = a[[0,1,2]] # copy
b4 = a[np.ones(1000, dtype=bool)] #copy
b5 = a[0, :] # view
b6 = a[:, 0] # view
b7 = a.T # view
b8 = a.flatten() # copy
b9 = a.ravel() # view

# print("a", a, "b1", b1, "b2", b2, "b3", b3, "b4", b4, "b5", b5, "b6", b6, "b7", b7, "b8", b8, "b9", b9, sep='\n')

b_list = [b1, b2, b3, b4, b5, b6, b7, b8, b9]

for i, b in enumerate(b_list, start = 1):
    print(f"a shares memory with b{i}" if np.shares_memory(a, b) else f"a doesn't share memory with b{i}")