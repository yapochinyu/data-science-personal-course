import numpy as np
a = np.arange(5)
b = a[1:4]
b[0] = 99
# что в a?
# в а изменится элемент под индексом 1
print(a)


a = np.arange(5)
c = a[a > 2]
c[0] = 99
# что в a?
# здесь а не изменится
print(a)


a = np.arange(5)
b = a[1:4].copy()
b[0] = 99

print(a)