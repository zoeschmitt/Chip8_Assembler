import re
import sys

labels = {}

def zerobin(fn):
	with open("rom.bin", "wb") as binary_file:
		binary_file.close()

def writebin(fn, b):
	with open("rom.bin", "ab") as binary_file:
        	binary_file.write(bytearray(b))

zerobin("rom.bin")

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
    instruction1 = ""
    instruction2 = ""


    if lineArgs[0] == "CLS":
        instruction1 = "00E0"
        instruction2 = format(0, '03b') + format(0, '03b') + format(14, '03b') + format(0, '03b')
        b = [0x00, 0, 14, 0]
    
    elif lineArgs[0] == "RET":
        instruction1 = "00EE"
        instruction2 = format(0, '02b') + format(0, '02b') + format(14, '03b') + format(14, '02b')
        b = [0x00, 0, 14, 14]

    elif lineArgs[0] == "SYS":
        if lineArgs[1][1:] in labels:
            reg = labels[lineArgs[1][1:]]
            instruction1 = "0" + str(labels[lineArgs[1][1:]])
            instruction2 = format(0, '02b') + format(labels[lineArgs[1][1:]], '03b')
            b = [0x00, 0, reg >> 8, reg & 0xFF]
        else:
            print("invalid label in SYS line")

    elif lineArgs[0] == "JP":
        if lineArgs[1][1:] in labels:
            reg = labels[lineArgs[1][1:]]
            instruction1 = "1" + str(labels[lineArgs[1][1:]])
            instruction2 = format(1, '02b') + format(labels[lineArgs[1][1:]], '03b')
            b = [0x01, 0, reg >> 8, reg & 0xFF]
        else:
            print("invalid label in JP line")

    elif lineArgs[0] == "CALL":
        if lineArgs[1][1:] in labels:
            reg = labels[lineArgs[1][1:]]
            instruction1 = "2" + str(labels[lineArgs[1][1:]])
            instruction2 = format(2, '02b') + format(labels[lineArgs[1][1:]], '03b')
            b = [0x02, 0, reg >> 8, reg & 0xFF]
        else:
            print("invalid label in CALL line")

    elif lineArgs[0] == "SE":
        if lineArgs[2][0] == "V":
            reg = int(lineArgs[1][1:])
            reg2 = int(lineArgs[2][1:])
            instruction1 = "5" + str(reg) + str(reg2) + "0"
            instruction2 = format(5, '02b') + format(reg, '03b') + format(reg, '03b') + format(0, '02b')
            b = [0x05, reg, reg2,0]

        elif lineArgs[2][0] != "V":
            reg = int(lineArgs[1][1:])
            val = int(lineArgs[2])
            instruction2 = format(3, '02b') + format(reg, '03b') + format(val, '03b')
            instruction1 = "3" + str(reg) + str(val >> 8) + str(val & 0xFF)
            b = [0x03, reg, val >> 8, val & 0xFF]

    elif lineArgs[0] == "SNE":
        if lineArgs[2][0] == "V":
            reg = int(lineArgs[1][1:])
            reg2 = int(lineArgs[2][1:])
            instruction1 = "9" + str(reg) + str(reg2) + "0"
            instruction2 = format(9, '02b') + format(reg, '03b') + format(reg2, '03b') + format(0, '02b')
            b = [0x09, reg, reg2,0]

        elif lineArgs[2][0] != "V":
            reg = int(lineArgs[1][1:])
            val = int(lineArgs[2])
            instruction2 = format(4, '02b') + format(reg, '03b') + format(val, '03b')
            instruction1 = "4" + str(reg) + str(val >> 8) + str(val & 0xFF)
            b = [0x04, reg, val >> 8, val & 0xFF]

    elif lineArgs[0] == "LD":

        if lineArgs[1][0] == "V":

            if lineArgs[2][0] == "V":
                reg = int(lineArgs[1][1:])
                reg2 = int(lineArgs[2][1:])
                instruction1 = "8" + str(reg) + str(reg2) + "0"
                instruction2 = format(8, '02b') + format(reg, '03b') + format(reg, '03b') + format(0, '02b')
                b = [0x08, reg, reg2, 0]

            elif lineArgs[2] == "DT":
                reg = int(lineArgs[1][1:])
                instruction1 = "F" + str(reg) + "07"
                instruction2 = format(15, '02b') + format(reg, '03b') + format(0, '02b') + format(7, '02b')
                b = [0x0F, reg, 0, 7]
            
            elif lineArgs[2][0] == "K":
                reg = int(lineArgs[1][1:])
                instruction1 = "F" + str(reg) + "0A"
                instruction2 = format(15, '02b') + format(reg, '03b') + format(0, '02b') + format(10, '02b')
                b = [0x0F, reg, 0, 10]

            elif lineArgs[2] == "[I]":
                reg = int(lineArgs[1][1:])
                instruction1 = "F" + str(reg) + "65"
                instruction2 = format(15, '02b') + format(reg, '03b') + format(6, '02b') + format(5, '02b')
                b = [0x0F, reg, 6, 5]

            elif lineArgs[2][0] != "V":
                reg = int(lineArgs[1][1:])
                val = int(lineArgs[2])
                instruction2 = format(6, '02b') + format(reg, '03b') + format(val, '03b')
                instruction1 = "6" + str(reg) + str(val >> 8) + str(val & 0xFF)
                b = [0x06, reg, val >> 8, val & 0xFF]

        elif lineArgs[1][0] == "I":
            if lineArgs[2][1:] in labels:
                reg = labels[lineArgs[2][1:]]
                instruction1 = "A" + str(labels[lineArgs[2][1:]])
                instruction2 = format(10, '02b') + format(labels[lineArgs[2][1:]], '03b')
                b = [0x0A, 0, reg >> 8, reg & 0xFF]
            else:
                print("invalid label in LD I line")

        elif lineArgs[1] == "[I]":
            reg = int(lineArgs[2][1:])
            instruction1 = "F" + str(reg) + "55"
            instruction2 = format(15, '02b') + format(reg, '03b') + format(5, '02b') + format(5, '02b')
            b = [0x0F, reg, 5, 5]

        elif lineArgs[1] == "F":
            reg = int(lineArgs[2][1:])
            instruction1 = "F" + str(reg) + "29"
            instruction2 = format(15, '02b') + format(reg, '03b') + format(2, '02b') + format(9, '02b')
            b = [0x0F, reg, 2, 9]

        elif lineArgs[1] == "B":
            reg = int(lineArgs[2][1:])
            instruction1 = "F" + str(reg) + "33"
            instruction2 = format(15, '02b') + format(reg, '03b') + format(3, '02b') + format(3, '02b')
            b = [0x0F, reg, 3, 3]

        elif lineArgs[1] == "DT":
            reg = int(lineArgs[2][1:])
            instruction1 = "F" + str(reg) + "15"
            instruction2 = format(15, '02b') + format(reg, '03b') + format(1, '02b') + format(5, '02b')
            b = [0x0F, reg, 1, 5]

        elif lineArgs[1] == "ST":
            reg = int(lineArgs[2][1:])
            instruction1 = "F" + str(reg) + "18"
            instruction2 = format(15, '02b') + format(reg, '03b') + format(1, '02b') + format(8, '02b')
            b = [0x0F, reg, 1, 8]

    elif lineArgs[0] == "ADD":
        if lineArgs[1][0] == "V":

            if lineArgs[2][0] == "V":
                reg = int(lineArgs[1][1:])
                reg2 = int(lineArgs[2][1:])
                instruction1 = "8" + str(reg) + str(reg2) + "4"
                instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(4, '02b')
                b = [0x08, reg, reg2, 4]

            elif lineArgs[2][0] != "V":
                reg = int(lineArgs[1][1:])
                val = int(lineArgs[2])
                instruction1 = "7" + str(reg) + str(val >> 8) + str(val & 0xFF)
                instruction2 = format(7, '02b') + format(reg, '03b') + format(val, '03b')
                b = [0x07, reg, val >> 8, val & 0xFF]

        if lineArgs[1][0] == "I":
            reg = int(lineArgs[2][1:])
            instruction1 = "F" + str(reg) + "1E"
            instruction2 = format(15, '02b') + format(reg, '03b') + format(1, '02b') + format(14, '02b')
            b = [0x0F, reg, 1, 14]

    elif lineArgs[0] == "OR":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "1"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(1, '02b')
        b = [0x08, reg, reg2, 1]

    elif lineArgs[0] == "AND":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "2"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(2, '02b')
        b = [0x08, reg, reg2, 2]

    elif lineArgs[0] == "XOR":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "3"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(3, '02b')
        b = [0x08, reg, reg2, 3]

    elif lineArgs[0] == "SUB":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "5"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(5, '02b')
        b = [0x08, reg, reg2, 5]

    elif lineArgs[0] == "SHR":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "6"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(6, '02b')
        b = [0x08, reg, reg2, 6]

    elif lineArgs[0] == "SUBN":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "7"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(7, '02b')
        b = [0x08, reg, reg2, 7]

    elif lineArgs[0] == "SHL":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        instruction1 = "8" + str(reg) + str(reg2) + "E"
        instruction2 = format(8, '02b') + format(reg, '03b') + format(reg2, '03b') + format(14, '02b')
        b = [0x08, reg, reg2, 14]

    elif lineArgs[0] == "RND":
        reg = int(lineArgs[1][1:])
        val = int(lineArgs[2])
        instruction2 = format(12, '02b') + format(reg, '03b') + format(val, '03b')
        instruction1 = "C" + str(reg) + str(val >> 8) + str(val & 0xFF)
        b = [0x0C, reg, val >> 8, val & 0xFF]

    elif lineArgs[0] == "DRW":
        reg = int(lineArgs[1][1:])
        reg2 = int(lineArgs[2][1:])
        n = int(lineArgs[3])
        instruction1 = "D" + str(reg) + str(reg2) + str(n)
        instruction2 = format(13, '02b') + format(reg, '03b') + format(reg2, '03b') + format(n, '03b')
        b = [0x0D, reg, reg2, n]

    elif lineArgs[0] == "SKP":
        reg = int(lineArgs[1][1:])
        instruction1 = "E" + str(reg) + "9E"
        instruction2 = format(14, '02b') + format(reg, '03b') + format(9, '02b') + format(14, '02b')
        b = [0x0E, reg, 9, 14]

    elif lineArgs[0] == "SKNP":
        reg = int(lineArgs[1][1:])
        instruction1 = "E" + str(reg) + "A1"
        instruction2 = format(14, '02b') + format(reg, '03b') + format(10, '02b') + format(1, '02b')
        b = [0x0E, reg, 10, 1]

    print("unformatted: " + instruction1)
    print("formatted: " + format(int(instruction2, 2), '04x'))
    print(b)
    writebin("rom.bin", b)


    
with open(sys.argv[1], 'r') as fp:
    lineNum = 0
    content = fp.read()
    lines = re.split("\n", content)
    
    for line in range (len(lines)):
        if lines[line][0] == ".":
            labels[lines[line][1:]] = lineNum * 4
        else: 
            lineNum = lineNum + 1
    
    for line in range (len(lines)):
        if lines[line][0] == ".":
            continue
        decode_assembly(lines[line])

    fp.close()

