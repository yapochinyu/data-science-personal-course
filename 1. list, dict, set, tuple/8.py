def dedup_keep_order(items):
    deduped_set = set()
    deduped_list = []
    for item in items:
        if item not in deduped_set:
            deduped_set.add(item)
            deduped_list.append(item)
    return deduped_list


if __name__ == '__main__':
    assert dedup_keep_order([3, 1, 2, 3, 10, -5, -5, 5, -5, 10, 11, 7]) == [3, 1, 2, 10, -5, 5, 11, 7]
    assert dedup_keep_order([]) == []
    assert dedup_keep_order([1, 1, 1]) == [1]
    assert dedup_keep_order([1, 2, 3]) == [1, 2, 3]

    print(dedup_keep_order([3, 1, 2, 3, 10, -5, -5, 5, -5, 10, 11, 7]))

    # решение через set(items) не подходит потому что set не упорядочен
