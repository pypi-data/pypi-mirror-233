def my_generator(param):
    if param:
        def inner_generator():
            yield 1
            yield 2
        return inner_generator
    else:
        def inner_generator():
            return 1
        return inner_generator

# Test
print(my_generator(True)()) # 输出：<generator object at 0x7f8c044a7850>
print(my_generator(False)()) # 输出: 1
