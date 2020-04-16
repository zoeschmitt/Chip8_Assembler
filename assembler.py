import re
import sys

def decode_assembly(line):
    lines_split = re.split(" |, |\(|\)", line)
    print(lines_split)
    args = []
    for txt in range (len(lines_split)):
        if (lines_split[txt] != ""):
            args.append(lines_split[txt])
    print(args)

    opcode = ""
    source = ""
    target = ""

    if (args[0] == "CLS"):
        opcode = "00E0"

    print(opcode)


    
with open(sys.argv[1], 'r') as fp:
    
    content = fp.read()
    lines = re.split("\n", content)
    print(lines)
    for line in range (len(lines)):
        decode_assembly(lines[line])

    fp.close()

