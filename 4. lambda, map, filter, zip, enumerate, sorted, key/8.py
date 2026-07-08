losses = [0.9, 0.7, 0.72, 0.5, 0.55, 0.3]

def spikes(losses):
    spikes = []
    for i, loss in enumerate(losses):
        if i == 0:
            pass
        elif loss > losses[i - 1]:
            spikes.append(i)
    return spikes

print(spikes(losses))