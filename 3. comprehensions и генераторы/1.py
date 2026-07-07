temps = [21.5, -3.0, 15.2, -7.8, 30.1, 0.0]

print([temp for temp in temps if temp > 0])

print([temp if temp >= 0 else 0 for temp in temps])

print([temp**2 if temp >= 0 else temp for temp in temps])