base = {'lr': 0.01, 'epochs': 100, 'batch_size': 32}
experiments = [{'lr': 0.1}, {'batch_size': 64}, {'lr': 0.001, 'epochs': 200}]

def model_fn(**kwargs):
    return kwargs


def run_all(model_fn, base, experiments):
    results = []
    for experiment in experiments:
        results.append(model_fn(**(base | experiment)))
    return results

print(run_all(model_fn, base, experiments))