raw = ['1.5', '2.7', 'NaN', '3.1', '', '4.0']

data = list(filter(lambda x : x != 'NaN', raw))
data = list(filter(lambda x : x != '', data))
data = list(map(float, data))
print(sum(data))

print(sum(float(x) for x in raw if x and x != 'NaN'))