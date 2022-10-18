""" 
    CONSTANTS
"""

from os import curdir
from tkinter import ALL
from typing import TYPE_CHECKING


DIGITS  =  '0123456789'

RTYPE   =  ['add', 'nand'] 
ITYPE   =  ['lw', 'sw', 'beq']
JTYPE   =  ['jalr']
OTYPE   =  ['halt', 'noop']

INTYPE    =  RTYPE+ITYPE+JTYPE+OTYPE

""" 
    ERROR
"""

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result = f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

""" 
    POSITION
"""

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col += 0
        
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

""" 
    TOKENS
"""

# define token type
TT_FUNC     = 'FUNC'
TT_RD       = 'RD'
TT_RS1      = 'RS1'
TT_RS2      = 'RS2'
TT_IMM      = 'IMM'

class Token:
    def __init__(self, text):
        self.text = text
        
    def __repr__(self):
        return f'{self.text}'

""" 
    LEXER
"""

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text.split()
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        
        self.current_val = 0
        self.func = None
        
    def advance(self):  # for moving current char to next char.
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in '\t':   # check if space or blank skip them.
                self.advance()
                    
            else:
                tokens.append(Token(self.current_char))
                self.advance()  
        
        return tokens, None
        
""" 
    RUN
"""
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error


# BUG NOW #

""" Ploblem1    <FIXED> <use isnumeric -> DIGITS>
    command > add 1 233 44
    File <stdin>, line 1    <- why use 233 will error?
    command > add 1 23 4
    [FUNC:add, RD:1, RS1:23, RS2:4]
    command > add 123 
    [FUNC:add, RD:123]
    command > add 1 233
    File <stdin>, line 1
    command > add 
"""