"""

This project was done with GREAT help from Craig Thomas's implementation of his own assembler
for super8 and chip8 emulators. His project was by far the best assembler I found during my research,
I think a great deal of it's effeciency (both in assembling and understandability) has to do with
the Python language. I was able to learn from his assembler to create an assembler for our chip8 emulator.

"""

"""
Imports explanation:

re: The re library (Regular expression operations) provides regular expression matching operations.
    i.e this library will help us to detect blank lines, comment lines, single line instructions,
    making sure a certain string is a register, etc

namedtuple from collections: collections are Python container datatypes that implement specialized
    container datatypes which provide alternatives to Python's general purpose built in containers.
    (in this case we are using them to create tuple subclasses with named fields, like: mnemonic, op,
    operands, sourse, target, and numeric in a tuple for an operation)

copy from copy: The Python language does not copy objects (like if you do x = c in C++, x now has a copy of c).
    Instead, it creates bindings between a target and object. Sometimes we just want a copy
    (when checking if syntax is correct) so we need to import copy.
"""
import re
from collections import namedtuple
from copy import copy

"""
TODO: explain the constants, why they need ot be constants.

x = s
kk = nn
y = t
"""

SOURCE = "source"
TARGET = "target"
NUMERIC = "numeric"
SOURCE_REG = "s"
TARGET_REG = "t"
NUMERIC_REG = "n"

"""
Constants using the re library that we imported.

BLANK_LINE: this is how we will be detecting blank lines in the input file.
COMMENT_LINE: this is how we will be detecting comment lines in the input file.
ASM_LINE: this is how we will be parsing a single line of code from the input file.
REGISTER_LINE: this is how we will be checking if an operand is a register.
"""

BLANK_LINE = re.compile(r"^\s*$")
COMMENT_LINE = re.compile(r"^\s*#\s*(?P<comment>.*)$")
ASM_LINE = re.compile(r"^(?P<label>\w*)\s+(?P<mnemonic>\w*)\s+(?P<operands>[\w$,+-]*)\s*[#]*\s*(?P<comment>.*)$")
REGISTER_LINE = re.compile("[rR][0-9a-fA-F]$")

"""
This Operation object is how we will be storing the lines that we take in from the input file.
What each field means:

instruction: holds the instruction name.
opcode: the instruction opcode.
operands: registers, values, and labels used in the operation.
source: this value signifies that their exists a "source" register in the operation. An example would
    be an operation that checks if a number is equal to a certain register (the source).
target: this value signifies that their exists a "target" register in the operation. If we use the
    example from above it would be that we're comparing another register to the source register, instead of just a number.
numeric: this value reflects the amount of numbers in an opcode for an operation, we will use this
    field to signify we must translate registers into hex values.
"""

Operation = namedtuple('Operation', ['instruction', 'opcode', 'operands', 'source', 'target', 'numeric'])

"""
These are all the operations that we are supporting project wide
"""

OPERATIONS = [
    Operation(opcode = "0nnn", operands = 1, source = 0, target = 0, numeric = 3, instruction = "SYS"),
    Operation(opcode = "00E0", operands = 0, source = 0, target = 0, numeric = 0, instruction = "CLR"),
    Operation(opcode = "00EE", operands = 0, source = 0, target = 0, numeric = 0, instruction = "RTS"),
    Operation(opcode = "1nnn", operands = 1, source = 0, target = 0, numeric = 3, instruction = "JUMP"),
    Operation(opcode = "2nnn", operands = 1, source = 0, target = 0, numeric = 3, instruction = "CALL"),
    Operation(opcode = "3snn", operands = 2, source = 1, target = 0, numeric = 2, instruction = "SKE"),
    Operation(opcode = "4snn", operands = 2, source = 1, target = 0, numeric = 2, instruction = "SKNE"),
    Operation(opcode = "5st0", operands = 2, source = 1, target = 1, numeric = 0, instruction = "SKRE"),
    Operation(opcode = "6snn", operands = 2, source = 1, target = 0, numeric = 2, instruction = "LOAD"),
    Operation(opcode = "7snn", operands = 2, source = 1, target = 0, numeric = 2, instruction = "ADD"),
    Operation(opcode = "8st0", operands = 2, source = 1, target = 1, numeric = 0, instruction = "MOVE"),
    Operation(opcode = "8st1", operands = 2, source = 1, target = 1, numeric = 0, instruction = "OR"),
    Operation(opcode = "8st2", operands = 2, source = 1, target = 1, numeric = 0, instruction = "AND"),
    Operation(opcode = "8st3", operands = 2, source = 1, target = 1, numeric = 0, instruction = "XOR"),
    Operation(opcode = "8st4", operands = 2, source = 1, target = 1, numeric = 0, instruction = "ADDR"),
    Operation(opcode = "8st5", operands = 2, source = 1, target = 1, numeric = 0, instruction = "SUB"),
    Operation(opcode = "8st6", operands = 1, source = 1, target = 1, numeric = 0, instruction = "SHR"),
    Operation(opcode = "8st7", operands = 2, source = 1, target = 1, numeric = 0, instruction = "SUBN"),
    Operation(opcode = "8stE", operands = 1, source = 1, target = 1, numeric = 0, instruction = "SHL"),
    Operation(opcode = "9st0", operands = 2, source = 1, target = 1, numeric = 0, instruction = "SKRNE"),
    Operation(opcode = "Annn", operands = 1, source = 0, target = 0, numeric = 3, instruction = "LOADI"),
    Operation(opcode = "Bnnn", operands = 1, source = 0, target = 0, numeric = 3, instruction = "JUMPI"),
    Operation(opcode = "Ctnn", operands = 2, source = 0, target = 1, numeric = 2, instruction = "RAND"),
    Operation(opcode = "Dstn", operands = 3, source = 1, target = 1, numeric = 1, instruction = "DRAW"),
    Operation(opcode = "Es9E", operands = 1, source = 1, target = 0, numeric = 0, instruction = "SKPR"),
    Operation(opcode = "EsA1", operands = 1, source = 1, target = 0, numeric = 0, instruction = "SKUP"),
    Operation(opcode = "Ft07", operands = 1, source = 0, target = 1, numeric = 0, instruction = "MOVED"),
    Operation(opcode = "Ft0A", operands = 1, source = 0, target = 1, numeric = 0, instruction = "KEYD"),
    Operation(opcode = "Fs15", operands = 1, source = 1, target = 0, numeric = 0, instruction = "LOADD"),
    Operation(opcode = "Fs18", operands = 1, source = 1, target = 0, numeric = 0, instruction = "LOADS"),
    Operation(opcode = "Fs1E", operands = 1, source = 1, target = 0, numeric = 0, instruction = "ADDI"),
    Operation(opcode = "Fs29", operands = 1, source = 1, target = 0, numeric = 0, instruction = "LDSPR"),
    Operation(opcode = "Fs33", operands = 1, source = 1, target = 0, numeric = 0, instruction = "BCD"),
    Operation(opcode = "Fs55", operands = 1, source = 1, target = 0, numeric = 0, instruction = "STOR"),
    Operation(opcode ="Fs65", operands = 1, source = 1, target = 0, numeric = 0, instruction = "READ")]


# psuedo operations ?? idk if needed
"""
    FCB = "FCB"
    FDB = "FDB"
    PSEUDO_OPERATIONS = [FCB, FDB]
"""

"""
The Translator function will be translating a single line of code (an Operation object) from the
input file by parsing it. The final product will be machine code for the emulator.
"""

class Translator(object):

    # Constructor
    def __init__(self):
        self.empty = True
        self.comment_only = False
        self.operation = None
        self.label = None
        self.operands = None
        self.comment = None
        self.size = 0
        self.address = None
        self.instruction = None
        self.op_code = None
        self.source = None
        self.target = None
        self.numeric = None

    # __str__ is used in Python for returning a custom string representation of a certain object (convenience).
    def __str__(self):
        return "0x{} {} {} {} {} # {}".format(
            self.get_address()[2:].upper().rjust(4, '0'),
            self.get_op_code().upper().rjust(4, '0'),
            self.get_label().rjust(10, ' '),
            self.get_instruction().rjust(5, ' '),
            self.get_operands().rjust(15, ' '),
            self.get_comment().ljust(40, ' ')
        )

    # in python, a static method is a method that doesnt alter the class state (doesnt change anything).
    # takes an operand and sees if their a register (starts with r or R)
    # if found, returns true, otherwise false.
    @staticmethod
    def is_register(string):
        if not REGISTER_LINE.match(string):
            return True
        else: 
            return False

    # if a string contains $ it returns a hex representation (register), if not, it returns the string (label).
    @staticmethod
    def get_value(string):
        if hex(int(string[1:], 16))[2:].upper().startswith("$"):
            return hex(int(string[1:], 16))[2:].upper()
        else: 
            return string

    @staticmethod
    def get_register(string):
        if not Translator.is_register(string):
            raise TrnaslationError("expected reg in r0 - rf but got [{}]".format(String))
        if len(string) > 2:
            raise TranslationError("invalid register [{}]".format(string))
        return hex(int(string[1:], 16))[-1].upper()

    
