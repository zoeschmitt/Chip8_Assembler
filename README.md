# Chip 8 Assembler

## Summary

This program takes an input file of assembly language code as an argument. It reads the contents and splits
each line into an array, then iterates through that array creating new arrays of each lines values. It then identifies
the proper opcode from there. It will write a binary file as output.
Prints array of each line and its identified opcode for testing convenience.

## How to run

Must have a working version of python installed.
In command line execute the follwing command: python assembler.py test.txt

## Resources

[Cowgods CHIP8 technical reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#00E0)
[Craig Thomas's implementation of a CHIP8 assembler](https://github.com/craigthomas/Chip8Assembler)
[Reed Foster's implementation of a simple assembler](https://hackaday.io/project/10576-mucpu-an-8-bit-mcu/log/36010-writing-an-assembler-in-python)
[Gary sims implementation of a simple assembler](https://github.com/garyexplains/examples/blob/master/vASM.py)
