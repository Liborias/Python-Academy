def podil(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(podil(6, 2))
