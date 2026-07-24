funcs = []
for i in range(3):
    funcs.append(lambda x, i=i: x * i)

funcs2 = []

def make_mult(i):
    return lambda x: x * i

for i in range(3):
    funcs2.append(make_mult(i))


if __name__ == '__main__':
    assert [f(10) for f in funcs] == [0, 10, 20]
    assert [f(10) for f in funcs2] == [0, 10, 20]
    print('OK')