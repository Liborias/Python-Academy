def minimum(data):
    if not data:
        return None
    nej = data[0]
    for x in data:
        if x < nej:
            nej = x
    return nej

print(minimum([3, 1, 2]))
