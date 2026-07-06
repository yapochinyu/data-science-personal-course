def log_metric(value, history=None):
    if history == None:
        history = []
    history.append(value)
    return history