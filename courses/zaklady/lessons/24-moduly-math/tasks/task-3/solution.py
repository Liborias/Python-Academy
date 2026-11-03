import math

def krabice(kusu, kapacita):
    return math.ceil(kusu / kapacita)

print(krabice(21, 10))
