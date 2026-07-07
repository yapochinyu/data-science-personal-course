def mean_latency(filepath):
    summ, count = 0, 0
    with open(filepath, 'r') as f:
        next(f) # для строки заголовка
        for line in f:
            summ += float(line.split(',')[2])
            count += 1
    return summ / count