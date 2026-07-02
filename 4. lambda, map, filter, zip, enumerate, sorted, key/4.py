raw = ['1.5', '2.7', 'NaN', '3.1', '', '4.0']

data = filter(lambda x: x and x != 'NaN', raw)
data = list(map(float, data))
print(sum(data))

print(sum(float(x) for x in raw if x and x != 'NaN'))