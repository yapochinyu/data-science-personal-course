def cat_to_idx(lst):
    return {cat: idx for idx, cat in enumerate(sorted(set(lst)))}


def idx_to_cat(mapping):
    return {idx: cat for cat, idx in mapping.items()}


if __name__ == '__main__':
    cats = ['cat', 'dog', 'cat', 'bird', 'dog']

    mapping = cat_to_idx(cats)
    assert mapping == {'bird': 0, 'cat': 1, 'dog': 2}

    reverse_mapping = idx_to_cat(mapping)
    assert reverse_mapping == {0: 'bird', 1: 'cat', 2: 'dog'}

    assert cat_to_idx([]) == {}
    assert idx_to_cat({}) == {}

    assert cat_to_idx(['a']) == {'a': 0}
    assert idx_to_cat({'a': 0}) == {0: 'a'}

    print(mapping)
    print(reverse_mapping)
