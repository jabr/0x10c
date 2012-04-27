# Math library for DCPU16

***NOTE: This is still in the R&D phase, and I have not yet implemented any of it in assembly. The initial prototypes are in Python, but they are designed to be efficiently portable to the DCPU.***

## floating point numbers

To avoid the overhead of bit-packing, I don't use any IEEE standard format. Instead, the numbers consist of two signed words. The first contains the mantissa/significand and the second the exponent.

The mantissa represents a fraction between -1 and 1. It's "value" is effectively `mantissa/32767`. The exponent is also signed (no basis), and represents a range from 2^(-32768) to 2^32766. 2^32767 (0x7fff) is a special case (infinity and NaN). This gives us a precision of ~3x10^(-5), and a ridiculous range of ~10^9863.

Exponent 0x7fff is a special case: if the mantissa is 0, it means NaN; otherwise, it represents infinity with the sign from the mantissa.

Basic arithmetic implementation should be simple and small; performance similar to a two word fixed point approach.

### Todo

Comparison functions: generally a few branching ops
ceil/floor: Branch on sign, then?
mod
remainder
abs: a hardware AND
inverse ?
flip: hardware XOR
constructor from base 10 ?
  needs log and exp
String format ?

Macro support for simple ops?

## math library

### Transcendentals

*** NOTE: The maths module (named to avoid conflict with the built-in math python module) is even more of a proof of concept. It currently uses python native floats, as I'm still working on the basic logic. A version using DCPU floats is coming soon.***

Anyway, most functions are based on the cordic algorithm. The core loop does 16 iterations on this simple logic:

    sign = z < 0 ? -1 : 1
    xt = x + sign * y >> i
    y = y - sign * x >> i
    z = z - sign * e[i]
    x = xt

`x, y, z` are fp numbers, and e is a lookup table of 16 fp numbers. Shifts on fps are a hardware SUB, and sign flipping on fps is a hardware XOR. Then there are three fp adds/subs.

sin/cos simultaneously in one cordic call.
tan adds a fp div on the sincos call

atan in one cordic.
2D hypot in one cordic, one fp mul.

atan2 is variable, some branching and generally one cordic, one fp div, and one fp add/sub when y is negative. no fp ops when x is 0.

2D cartesian to polar transform is one cordic, one fp mul, some branching, and one fp add/sub when x is negative.

Limited domain exp, log, sqrt in one cordic (though a 21 iteration version), one fp mul or add.

It should be possible to expand the domain for exp/log with an additional fp mul and add.

## Other functions

A more robust sqrt using Newton's Iteration:

Variable number of iterations of:
`k = (k + n/k) >> 1`

One fp div and add, plus a hardware SUB.

Iteration count is either fixed (parameter) or loops until convergence using a fp sub (and fp abs - a hardware AND).

## In search of better exp/log

Can we use the cordic functions in a broader range?

If not, is there a different approach to approximating these functions?

# Contributing

Pull requests are very welcome!

