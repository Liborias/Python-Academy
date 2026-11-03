def bezpecne_del(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(bezpecne_del(8, 2))
