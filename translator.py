"""
Imports explanation:

re: The re library (Regular expression operations) provides regular expression matching operations. i.e this library will help us to detect blank lines, comment lines, single line instructions, making sure a certain string is a register, etc

namedtuple from collections: collections are Python container datatypes that implement specialized container datatypes which provide alternatives to Python's general purpose built in containers. (in this case we are using them to create tuple subclasses with named fields, like: mnemonic, op, operands, sourse, target, and numeric in a tuple for an operation)

copy from copy: The Python language does not copy objects (like if you do x = c in C++, x now has a copy of c). Instead, it creates bindings between a target and object. Sometimes we just want a copy (when checking if syntax is correct) so we need to import copy.
"""
import re
from collections import namedtuple
from copy import copy

"""
TODO: explain the constants, why they need ot be constants.
"""

SOURCE = "source"
TARGET = "target"
NUMERIC = "numeric"
SOURCE_REG = "s"
TARGET_REG = "t"
NUMERIC_REG = "n"

"""
This Operation object is how we will be storing the lines that we take in from the input file.
"""

Operation = namedtuple('Operation', ['instruction', 'opcode', 'operands', 'source', 'target', 'numeric'])

OPERATIONS = [
    Operation(opcode = "0nn")]




