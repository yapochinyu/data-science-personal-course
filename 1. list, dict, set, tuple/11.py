s = {1, 2, 3, 4, 5}

for x in s.copy():
    if x % 2 == 0:
        s.remove(x)

print(s)


s = {1, 2, 3, 4, 5}

print({x for x in s if x % 2 != 0})