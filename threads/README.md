# cooperative threading for DCPU16

This is a basic implementation of a cooperative thread model for DCPU16. The code compiles on common assemblers, and includes a simple example program at the top of the core.ds file. It runs a main thread that launches a second (then later third) thread. The threads simply increment their local I register, and display the current thread "type" (1 or 2) on the screen (i.e. write the character to 0x8000). If you're watching memory as the program runs, you can see the incrementing I registers near the end of memory (on the stack).

## Notes

* Following the pseudo-standard consensus, only the XYZIJ registers are preserved between calls (and yields). ABC are generally clobbered.
* Thread stacks are not preserved, so it only makes sense to yield from the top level "thread main". A thread start or resume should assume the stack is empty.
* The preceding two points mean that a thread can only store state through a yield in XYZIJ registers.
* Finally, the maximum number of threads must be declared with the thread manager is initialized. If that number is exceeded, the create "function" will return -1 (0xffff) in the A register. Otherwise, create will return with the thread number in A.
