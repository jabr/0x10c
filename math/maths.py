#!/usr/bin/env python

from __future__ import division
import sys, math

values = map(float, sys.argv[1:])

anglesN = (
    0.78539816339745, 0.46364760900081, 0.24497866312686, 0.12435499454676,
    0.06241880999596, 0.03123983343027, 0.01562372862048, 0.00781234106010,
    0.00390623013197, 0.00195312251648, 0.00097656218956, 0.00048828121119,
    0.00024414062015, 0.00012207031189, 0.00006103515617, 0.00003051757812,
)

anglesH = (
    0.54930614433405, 0.25541281188300, 0.12565721414045, 0.06258157147700,
    0.03126017849067, 0.01562627175205, 0.00781265895154, 0.00390626986840,
    0.00195312748353, 0.00097656281044, 0.00048828128881, 0.00024414062985,
    0.00012207031311, 0.00006103515633, 0.00003051757813, 0.00001525878906,
)

Kn = 0.60725293500888
Kh = 1.20753449527637

pi = math.pi
halfpi = math.pi/2

def cordic(x, y, z):
    for i in range(16):
        s = -1 if z < 0 else 1
        t = 2.0**(-1 * i)
        x, y = x - s * y * t, y + s * x * t
        z = z - s * anglesN[i]
    return x, y, z

def icordic(x, y, z):
    for i in range(16):
        s = -1 if y >= 0 else 1
        t = 2.0**(-1 * i)
        x, y = x - s * y * t, y + s * x * t
        z = z - s * anglesN[i]
    return x, y, z

def hcordic(x, y, z):
    for i in range(16):
        times = 2 if i in (3,6,9,12,15) else 1
        for _ in range(times):
            s = -1 if z < 0 else 1
            t = 2.0**(-1 * (i + 1))
            x, y = x + s * y * t, y + s * x * t
            z = z - s * anglesH[i]
    return x, y, z

def ihcordic(x, y, z):
    for i in range(16):
        times = 2 if i in (3,6,9,12,15) else 1
        for _ in range(times):
            s = -1 if y >= 0 else 1
            t = 2.0**(-1 * (i + 1))
            x, y = x + s * y * t, y + s * x * t
            z = z - s * anglesH[i]
    return x, y, z

def sincos(radians):
    if radians < -halfpi or radians > halfpi:
        if radians < 0:
            s, c = sincos(radians + pi)
        else:
            s, c = sincos(radians - pi)
        return -s, -c
    c, s, _ = cordic(Kn, 0.0, radians)
    return s, c

def tan(radians):
    s, c = sincos(radians)
    return s/c

def atan(v):
    _, _, a = icordic(1, v, 0)
    return a

def atan2(y, x):
    if x == 0:
        if y == 0:
            return 0
        return halfpi if y > 0 else -halfpi
    a = atan(y/x)
    if x > 0:
        return a
    if y < 0:
        a -= pi
    else:
        a += pi
    return a

def hypot(x, y):
    a, _, _ = icordic(x, y, 0)
    return a * Kn

def polar(x, y):
    invert = False
    if x < 0:
        invert = True
        x = -x
        y = -y
    d, _, a = icordic(x, y, 0)
    if invert:
        if y < 0:
            a -= pi
        else:
            a += pi
    return d * Kn, a

def exp(v): # v <= 1
    a, b, _ = hcordic(Kh, 0, v)
    return a + b

def sqrt(v): # 0.03 < v < 2
    a, _, _ = ihcordic(v + 0.25, v - 0.25, 0)
    return a * Kh

def log(v): # 0.1 < a < 9.58
    _, _, a = ihcordic(v + 1, v - 1, 0)
    return a * 2

# alternate approaches:

# Newton's Iteration
def n_sqrt(v):
    k = 1
    pk = 0
    count = 0
    iterations = max(16, int(math.log(v)) * 3)
    # for i in range(iterations):
    while pk != k:
        count += 1
        pk = k
        k = (k + v/k) / 2
    print(count, iterations)
    return k

if __name__ == '__main__':
    for x in values:
        if math.fabs(x) < 10000:
            rx = x * pi / 180
            s, c = sincos(rx)

            v = s
            n = math.sin(rx)
            print "sin\n = {}\n o {} {}".format(v, n, n-v)

            v = c
            n = math.cos(rx)
            print "cos\n = {}\n o {} {}".format(v, n, n-v)

            v = tan(rx)
            n = math.tan(rx)
            print "tan\n = {}\n o {} {}".format(v, n, n-v)

        v = atan(x)
        n = math.atan(x)
        print "atan\n = {} {}\n o {} {}".format(v, v * 180 / pi, n, n-v)

        v = exp(x)
        try:
            n = math.exp(x)
        except:
            n = float('nan')
        print "exp\n = {}\n o {} {}".format(v, n, n-v)

        v = sqrt(x)
        try:
            n = math.sqrt(x)
        except:
            n = float('nan')
        print "sqrt\n = {}\n o {} {}".format(v, n, n-v)

        v = n_sqrt(x)
        print "n_sqrt\n = {}\n o {} {}".format(v, n, n-v)

        v = log(x)
        try:
            n = math.log(x)
        except:
            n = float('nan')
        print "log\n = {}\n o {} {}".format(v, n, n-v)

    if len(values) > 1:
        x, y = values[:2]

        v = atan2(x, y)
        n = math.atan2(x, y)
        print "atan2\n = {} {}\n o {} {}".format(v, v * 180 / pi, n, n-v)

        v, n = polar(x, y)
        print "polar\n = {} {} {}".format(v, n, n * 180 / pi)

        v = hypot(x, y)
        n = math.hypot(x, y)
        print "hypot\n = {}\n o {} {}".format(v, n, n-v)
