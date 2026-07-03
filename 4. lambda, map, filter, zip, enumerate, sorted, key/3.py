def top_scores(scores, n):
    scores.sort(reverse=True)
    return scores[:n]


def top_scores_no_rewrite(scores, n):
    return sorted(scores, reverse=True)[:n]


if __name__ == '__main__':
    assert top_scores([3, 1, 2], 2) == [3, 2]
    assert top_scores_no_rewrite([3, 1, 2], 2) == [3, 2]
    assert top_scores_no_rewrite([], 2) == []
    assert top_scores_no_rewrite([5], 3) == [5]

    print(top_scores([3, 1, 2], 2))
    print(top_scores_no_rewrite([3, 1, 2], 2))

    # вариант без переписывания исходного списка логичнее,
    # потому что функция не должна преобразовывать исходные данные,
    # если также возвращает и результат,
    # либо одно, либо другое, оба варианта не нужны.
