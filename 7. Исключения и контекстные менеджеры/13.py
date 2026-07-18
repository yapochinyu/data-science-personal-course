# #LBYL
# if x in cache:
#     val = cache[x]
# else:
#     val = compute(x)
#     cache[x] = val

# #EAFP
# try:
#     val = cache[x]
# except KeyError:
#     val = compute(x)
#     cache[x] = val

# #idiom
# val = cache[x] if x in cache else cache.setdefault(x, compute(x))