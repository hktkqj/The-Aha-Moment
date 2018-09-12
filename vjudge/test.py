from math import *


def calc(d, delta):
    left = 0
    r = 10000000000
    now = 0
    while abs(now-delta) > 0.0000000001:
        mid = (left+r) / 2
        now = mid * cosh(d/mid) - mid
        if now < delta:
            r = mid
        else:
            left = mid
    return mid


def h(a, x):
    return a * sinh(x/a) * 2


if __name__ == '__main__':
    while True:
        str1 = input()
        p = float(str1.split(' ')[0])
        if p == -1:
            break
        d = float(str1.split(' ')[1])
        print("%.3f" % (floor(1000*h(calc(d/2, p-4.2), d/2))/1000))
