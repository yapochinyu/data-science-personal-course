def log_metric(value, history=None):
    if history is None:
        history = []
    history.append(value)
    return history