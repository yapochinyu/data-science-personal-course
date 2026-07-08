names = ['Alice', 'Bob', 'Charlie', 'David']
scores = [88, 95, 88, 70]

print([name for name, score in sorted(zip(names, scores), key=lambda x: (-x[1], x[0]))])
