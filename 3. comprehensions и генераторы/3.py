a = [x*2 for x in range(3)]
b = {x*2 for x in range(3)}
c = {x: x*2 for x in range(3)}
d = (x*2 for x in range(3))
e = tuple(x*2 for x in range(3))

print(a)
print(b)
print(c)
print(d)
print(e)
