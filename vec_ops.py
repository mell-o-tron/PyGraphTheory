import math

##### 2D vector operations #####
def vectorSum(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def vectorMul(a, k):
    return [a[0] * k, a[1] * k]

def vectorDistance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def vectorCeil(a):
    return [math.ceil(a[0]), math.ceil(a[1])]

def vectorFloor(a):
    return [math.floor(a[0]), math.floor(a[1])]

def vectorSign(a):
    if a[0] >= 0 and a[1] >= 0:
        return 1
    else:
        return -1
