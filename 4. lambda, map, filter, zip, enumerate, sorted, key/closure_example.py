funcs_late = [lambda x: x * i for i in range(3)]

for f in funcs_late:
    assert f.__closure__ is not None
    print(id(f.__closure__[0]))

print([f(10) for f in funcs_late])

funcs_early = [lambda x, i=i: x * i for i in range(3)]
print([f(10) for f in funcs_early])


if __name__ == '__main__':
    assert [f(10) for f in funcs_late] == [20, 20, 20]
    assert [f(10) for f in funcs_early] == [0, 10, 20]
    print('all tests passed')