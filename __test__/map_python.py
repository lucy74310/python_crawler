a = [1, 2, 3, 4]


def f(x):
    return x**2


it = map(lambda x: print(x**2, end=' '), [1, 2, 3, 4])

next(it)
next(it)
next(it)
next(it)

print('\n====================')
list(map(lambda x: print(x**2, end=' '), [1, 2, 3, 4]))


# filter
print('\n====================')
lst = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
print(lst)


print('\n====================')









