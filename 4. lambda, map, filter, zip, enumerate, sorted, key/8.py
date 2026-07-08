losses = [0.9, 0.7, 0.72, 0.5, 0.55, 0.3]

def spikes(losses):
    spikes = [i for i, (prev, curr) in enumerate(zip(losses, losses[1:]), start=2) 
              if prev < curr]
    return spikes

print(spikes(losses))