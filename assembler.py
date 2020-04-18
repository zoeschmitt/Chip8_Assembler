import re
import sys

def decode_assembly(line):
    lines_split = re.split(" |, |\(|\)", line)
    print(lines_split)
    lineArgs = []
    for txt in range (len(lines_split)):
        if (lines_split[txt] != ""):
            lineArgs.append(lines_split[txt])
    print(lineArgs)

    op = ""
    reg = ""
    reg2 = ""
    val = ""
    instruction = ""

    if lineArgs[0] == "CLS":
        instruction = "00E0"
    
    elif lineArgs[0] == "RET":
        instruction = "00EE"

    elif lineArgs[0] == "SYS":
        op = ""

    elif lineArgs[0] == "JP":
        op = ""

    elif lineArgs[0] == "CALL":
        op = ""

    elif lineArgs[0] == "SE":
        op = ""

    elif lineArgs[0] == "SNE":
        op = ""

    elif lineArgs[0] == "LD":

        if lineArgs[1][0] == "V":

            if lineArgs[2][0] == "V":
                reg = int(lineArgs[1][1])
                reg2 = int(lineArgs[2][1])
                instruction = "8" + str(reg) + str(reg2) + "0"

            elif lineArgs[2] == "DT":
                reg = int(lineArgs[1][1])
                instruction = "F" + str(reg) + "07"
            
            elif lineArgs[2][0] == "K":
                reg = int(lineArgs[1][1])
                instruction = "F" + str(reg) + "0A"

            elif lineArgs[2][0] != "V":
                reg = int(lineArgs[1][1])
                val = int(lineArgs[2])
                instruction = [0x00, reg, val >> 8, val & 0xFF]
                print(bytearray(instruction))
                instruction = "6" + str(reg) + str(val >> 8) + str(val & 0xFF)

    elif lineArgs[0] == "ADD":
        op = ""

    elif lineArgs[0] == "OR":
        op = ""

    elif lineArgs[0] == "AND":
        op = ""

    elif lineArgs[0] == "XOR":
        op = ""

    elif lineArgs[0] == "SUB":
        op = ""

    elif lineArgs[0] == "SHR":
        op = ""

    elif lineArgs[0] == "SUBN":
        op = ""

    elif lineArgs[0] == "SHL":
        op = ""

    elif lineArgs[0] == "RND":
        op = ""

    elif lineArgs[0] == "DRW":
        op = ""

    elif lineArgs[0] == "SKP":
        op = ""

    elif lineArgs[0] == "SKNP":
        op = ""

    print(instruction)


    
with open(sys.argv[1], 'r') as fp:
    
    content = fp.read()
    lines = re.split("\n", content)
    print(lines)
    for line in range (len(lines)):
        decode_assembly(lines[line])

    fp.close()

