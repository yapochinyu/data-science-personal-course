def count_pairs(a: list[int], k: int) -> int:
    count = 0
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] + a[j] <= k:
                count += 1
    return count

def count_pairs_v2(a: list[int], k: int) -> int:
    count = 0
    i, j = 0, len(a) - 1
    while i != j:
        

    return count


if __name__ == '__main__':
