# cooperative threading for DCPU16

This is a hypothetical implementation of a cooperative thread model for DCPU16. The code doesn't actually compile on most assemblers at the moment, as it uses some custom commands and syntax.

## Notes

* Following the pseudo-standard consensus, only the XYZIJ registers are preserved between calls (and yields). ABC are generally clobbered.
* Thread stacks are not preserved, so it only makes sense to yield from the top level "thread main". A thread start or resume should assume the stack is empty.
* The preceding two points mean that a thread can only store state through a yield in XYZIJ registers.
* Finally, the maximum number of threads must be declared with the thread manager is initialized. If that number is exceeded, the create "function" will return -1 (0xffff) in the A register. Otherwise, create will return with the thread number in A.
