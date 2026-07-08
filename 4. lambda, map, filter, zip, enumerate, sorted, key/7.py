grades = [
    [5, 4, 3], 
    [4, 4, 5], 
    [3, 5, 4]
    ]


mean_by_subject = [sum(col) / len(col) for col in zip(*grades)]
print(mean_by_subject)