import math

def vec(x, y, ex, ey, mag):
    i = ex - x
    j = ey - y
    m = math.sqrt((i * i) + (j * j))
    ic = i / m
    jc = j / m
    return ((ic * mag), (jc * mag))
