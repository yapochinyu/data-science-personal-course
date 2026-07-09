from itertools import combinations

points = [(1, 2), (3, 4), (0, 0), (5, 1)]

def dist(x1, y1, x2, y2): 
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5

longest = max(combinations(points, 2), key=lambda pair: dist(*pair[0], *pair[1]))

print(longest)