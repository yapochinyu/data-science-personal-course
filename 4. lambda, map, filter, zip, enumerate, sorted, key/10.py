words = ['pear', 'fig', 'apple', 'kiwi', 'date']

print(sorted(words, key=lambda x: (len(x), x.lower())))
print(sorted(words, key=lambda x: (-len(x), x.lower())))