def group_by_first_letter(words):
    first_letter = {}
    for word in words:
        if word[0] not in first_letter:
            first_letter[word[0]] = [word]
        else:
            first_letter[word[0]].append(word)
    return first_letter


def group_by_first_letter_with_default(words):
    first_letter = {}
    for word in words:
        first_letter.setdefault(word[0], []).append(word)
    return first_letter


if __name__ == '__main__':
    words = ["apple", "banana", "avocado", "cherry", "blueberry"]
    expected = {
        "a": ["apple", "avocado"],
        "b": ["banana", "blueberry"],
        "c": ["cherry"],
    }

    assert group_by_first_letter(words) == expected
    assert group_by_first_letter_with_default(words) == expected

    assert group_by_first_letter([]) == {}
    assert group_by_first_letter_with_default([]) == {}

    assert group_by_first_letter(["dog"]) == {"d": ["dog"]}
    assert group_by_first_letter_with_default(["dog"]) == {"d": ["dog"]}

    assert group_by_first_letter(["ant", "ant", "bee"]) == {"a": ["ant", "ant"], "b": ["bee"]}
    assert group_by_first_letter_with_default(["ant", "ant", "bee"]) == {"a": ["ant", "ant"], "b": ["bee"]}

    print("все тесты прошли")