"""
ASSEMBLER
This program takes an input file full of assembly language code as an argument. It reads the contents and splits
each line into an array, then iterates through that array creating arrays of each value in a line and
identifies the proper opcode from there.
It will write a binary file as output.
"""

import re
import sys

"""
The labels dictionary will be holding the label name and its location.
"""
labels = {}

def zerobin(fn):
	with open("pong.ch8", "wb") as file:
		file.close()

def writebin(fn, b):
	with open("pong.ch8", "ab") as file:
        	file.write(bytearray(b))

zerobin("pong.ch8")

"""
This function is called for each line in the input file, it seperates each of the values in
the original array of lines into their own array. Then it identifies the instruction, registers,
and values associated if any.
"""
def decode_assembly(line):
    lines_split = re.split(" |, |\(|\)", line)
    #print(lines_split)
    lineArgs = []
    for txt in range (len(lines_split)):
        if (lines_split[txt] != ""):
            lineArgs.append(lines_split[txt])
    print(lineArgs)

    b = ""
    reg = ""
    reg2 = ""
    val = ""
    addr = ""


    if lineArgs[0] == "CLS":
        b = [0x00, 0, 14, 0]
    
    elif lineArgs[0] == "RET":
        b = [0x00, 0, 14, 14]

    elif lineArgs[0] == "SYS":
        if lineArgs[1][0:] in labels:
            addr = labels[lineArgs[1][0:]]
            b = [0x0, addr >> 8, addr >> 8, addr & 0xFF]
        else:
            print("invalid label in SYS line")

    elif lineArgs[0] == "JP":
        if lineArgs[1][0:] in labels:
            addr = labels[lineArgs[1][0:]]
            b = [0x1, addr >> 8, addr >> 8, addr & 0xFF]
        else:
            print("invalid label in JP line")

    elif lineArgs[0] == "CALL":
        if lineArgs[1][0:] in labels:
            addr = labels[lineArgs[1][0:]]
            b = [0x2, addr >> 8, addr >> 8, addr & 0xFF]
        else:
            print("invalid label in CALL line")

    elif lineArgs[0] == "SE":
        if lineArgs[2][0] == "V":
            reg = int(lineArgs[1][1:])
            reg2 = int(lineArgs[2][1:])
            b = [0x5, reg, reg2,0]

        elif lineArgs[2][0] != "V":
            reg = int(lineArgs[1][1:])
            val = int(lineArgs[2])
            b = [0x3, reg, val >> 8, val & 0xFF]

    elif lineArgs[0] == "SNE":
        if lineArgs[2][0] == "V":
            reg = int(lineArgs[1][1:])
            reg2 = int(lineArgs[2][1:])
            b = [0x9, reg, reg2,0]

        elif lineArgs[2][0] != "V":
            reg = int(lineArgs[1][1:])
            val = int(lineArgs[2])
            b = [0x4, reg, val >> 8, val & 0xFF]

    elif lineArgs[0] == "LD":

        if lineArgs[1][0] == "V":

            if lineArgs[2][0] == "V":
                reg = int(lineArgs[1][1:])
                reg2 = int(lineArgs[2][1:])
                b = [0x8, reg, reg2, 0]

            elif lineArgs[2] == "DT":
                reg = int(lineArgs[1][1:])
                b = [0xF, reg, 0, 7]
            
            elif lineArgs[2][0] == "K":
                reg = int(lineArgs[1][1:])
                b = [0xF, reg, 0, 10]

            elif lineArgs[2] == "[I]":
                reg = int(lineArgs[1][1:])
                b = [0xF, reg, 6, 5]

            elif lineArgs[2][0] != "V":
                reg = int(lineArgs[1][1:])
                val = int(lineArgs[2])
                b = [0x6, reg, val >> 8, val & 0xFF]

        elif lineArgs[1][0] == "I":
            addr = int(lineArgs[2][0:])
            b = [0xA, addr >> 8, addr >> 8, addr & 0xFF]

        elif lineArgs[1] == "[I]":
            reg = int(lineArgs[2][1:])
            b = [0xF, reg, 5, 5]

        elif lineArgs[1] == "F":
            reg = int(lineArgs[2][1:])
            b = [0xF, reg, 2, 9]

        elif lineArgs[1] == "B":
            reg = int(lineArgs[2][1:])
            b = [0xF, reg, 3, 3]

        elif lineArgs[1] == "DT":
            reg = int(lineArgs[2][1:])
            b = [0xF, reg, 1, 5]

        elif lineArgs[1] == "ST":
            reg = int(lineArgs[2][1:])
            b = [0xF, reg, 1, 8]

    elif lineArgs[0] == "ADD":
        if lineArgs[1][0] == "V":

            if lineArgs[2][0] == "V":
                reg = int(lineArgs[1][1:])
                reg2 = int(lineArgs[2][1:])
                b = [0x8, reg, reg2, 4]

            elif lineArgs[2][0] != "V":
                reg = int(lineArgs[1][1:])
                val = int(lineArgs[2])
                b = [0x7, reg, val >> 8, val & 0xFF]

        if lineArgs[1][0] == "I":
            reg = int(lineArgs[2][1:])
            b = [0xF, reg, 1, 14]

    elif lineArgs[0] == "OR":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x8, reg, reg2, 1]

    elif lineArgs[0] == "AND":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x8, reg, reg2, 2]

    elif lineArgs[0] == "XOR":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x8, reg, reg2, 3]

    elif lineArgs[0] == "SUB":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x8, reg, reg2, 5]

    elif lineArgs[0] == "SHR":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x8, reg, reg2, 6]

    elif lineArgs[0] == "SUBN":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x08, reg, reg2, 7]

    elif lineArgs[0] == "SHL":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        b = [0x8, reg, reg2, 14]

    elif lineArgs[0] == "RND":
        reg = int(lineArgs[1][1:])
        val = int(lineArgs[2])
        b = [0xC, reg, val >> 8, val & 0xFF]

    elif lineArgs[0] == "DRW":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        n = int(lineArgs[3])
        b = [0xD, reg, reg2, n]

    elif lineArgs[0] == "SKP":
        reg = int(lineArgs[1][1:])
        b = [0xE, reg, 9, 14]

    elif lineArgs[0] == "SKNP":
        reg = int(lineArgs[1][1:])
        b = [0xE, reg, 10, 1]

    print(b)

    writebin("pong.ch8", b)

"""
This code runs first. It takes the arugment from the command line (input file), reads the input file contents
into an array, and then runs through the lines to record the labels and their locations. It then calls decode_assembly
for each line, making sure to skip label lines in the process.
"""
with open(sys.argv[1], 'r') as fp:
    lineNum = 0
    content = fp.read()
    lines = re.split("\n", content)
    
    for line in range (len(lines)):
        if lines[line][0] == ".":
            labels[lines[line][1:]] = lineNum * 4
        else: 
            lineNum = lineNum + 1
    print(labels)
    for line in range (len(lines)):
        if lines[line][0] == ".":
            continue
        decode_assembly(lines[line])

    fp.close()

