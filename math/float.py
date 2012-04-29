#!/usr/bin/env python

from __future__ import division
import sys, math

(a,b) = map(float, sys.argv[1:])

def to(v):
    try:
        e = int(math.ceil(math.log(math.fabs(v), 2)))
    except:
        e = 0
    s = int(math.ceil((v / math.pow(2, e)) * 0x7fff))
    return (s, e)

def normalize(f, e):
    while abs(f) > 0x7fff:
        f >>= 1
        e += 1

    while abs(f) < 0x4000:
        f <<= 1
        e -= 1

    if (e < -0x7fff):
        f = e = 0
    if (e >= 0x7fff):
        f = math.copysign(0x7fff, f)
        e = 0x7fff
    return (f, e)

def add(a, b):
    (af, ae) = to(a)
    (bf, be) = to(b)

    d = int(ae - be)
    if (d < 0):
        s = -d
        af >>= s
        return normalize(af + bf, be)
    else:
        bf >>= d
        return normalize(af + bf, ae)

def sub(a, b):
    (af, ae) = to(a)
    (bf, be) = to(b)

    d = int(ae - be)
    if (d < 0):
        s = -d
        af >>= s
        return normalize(af - bf, be)
    else:
        bf >>= d
        return normalize(af - bf, ae)

def mul(a, b):
    (af, ae) = to(a)
    (bf, be) = to(b)

    mf = (af * bf) >> 15
    me = ae + be
    return normalize(mf, me)

def div(a, b):
    (af, ae) = to(a)
    (bf, be) = to(b)

    if bf == 0:
        return (0, 0x7fff) # nan

    mf = (af / bf) * 0x7fff
    me = ae - be
    return normalize(int(mf), me)

def to_float(af, ae):
    if (af > 0x7fff):
        af = -(0xffff - af)
    return (af / 0x7fff) * math.pow(2, ae)

def conversion_details(a):
    (af, ae) = to(a)
    print "{} = {}b{}\n = {:04x} {:04x} = {:016b} {:016b}\n = {}".format(
        a, af, ae,
        af & 0xffff, ae & 0xffff,
        af & 0xffff, ae & 0xffff,
        to_float(af, ae)
    )

conversion_details(a)
conversion_details(b)

def number_details(af, ae):
    print "{}b{} = {}\n = {:04x} {:04x} = {:016b} {:016b}".format(
        af, ae, to_float(af, ae),
        af & 0xffff, ae & 0xffff,
        af & 0xffff, ae & 0xffff,
    )

print "\n"

(mf, me) = mul(a, b)
print "a * b"
number_details(mf, me)

(mf, me) = div(a, b)
print "a / b"
number_details(mf, me)

(mf, me) = add(a, b)
print "a + b"
number_details(mf, me)

(mf, me) = sub(a, b)
print "a - b"
number_details(mf, me)
