def make_threshold_filter(threshold):
    def threshold_filter(nums):
        filtered = [num for num in nums if num > threshold]
        return filtered
    return threshold_filter


strict = make_threshold_filter(0.9)
loose = make_threshold_filter(0.5)

data = [0.4, 0.6, 0.95]

print(strict(data))
print(loose(data))

print(strict.__closure__[0].cell_contents)