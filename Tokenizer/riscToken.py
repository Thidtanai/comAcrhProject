""" 
    CONSTANTS
"""

from mimetypes import common_types
from os import curdir
from tkinter import ALL
from typing import TYPE_CHECKING
from typing_extensions import Self
from xml.etree.ElementTree import Comment


DIGITS  =  '0123456789'

RTYPE   =  ['add', 'nand'] 
ITYPE   =  ['lw', 'sw', 'beq']
JTYPE   =  ['jalr']
OTYPE   =  ['halt', 'noop']
SPTYPE  =  ['.fill']

ISOP    =  RTYPE+ITYPE+JTYPE+OTYPE+SPTYPE

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
TT_LABEL    = 'label'

TT_INST     = 'instruction'

TT_REGA     = 'regA'
TT_REGB     = 'regB'
TT_DREG     = 'destReg'
TT_OFSET    = 'ofset'

TT_COMNT    = 'comment'
TT_NON      = 'nonField'

TT_ID      = 'index'

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

""" 
    LEXER
"""

class Lexer:
    def __init__(self, fn, text, index):
        self.fn = fn
        self.text = text.split()
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

        self.index = index
        
        self.current_loop = 0
        self.inst = None
        self.symbolic = False
        self.not_comment = True
        
    def advance(self):  # for moving current char to next char.
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        comment = ""
        current_loop = 0
        tokens.append(Token(TT_ID, self.index))

        while current_loop < 6 or current_loop <= len(self.text):
            if self.current_char in ISOP:   # check it is opcode.
                if current_loop == 0:
                    tokens.append(Token(TT_NON))
                    current_loop += 1
                tokens.append(Token(TT_INST, self.current_char))
                self.inst = self.current_char
                current_loop += 1
                self.advance()  
            
            elif current_loop == 0:    # check it has label
                tokens.append(Token(TT_LABEL, self.current_char))
                current_loop += 1
                self.advance()
            
            elif self.not_comment: #check it not comment
                if self.inst in RTYPE:
                    if current_loop == 2: tokens.append(Token(TT_REGA, self.current_char))
                    elif current_loop == 3: tokens.append(Token(TT_REGB, self.current_char))
                    elif current_loop == 4: 
                        tokens.append(Token(TT_DREG, self.current_char))
                        self.not_comment = False
                    else: print("error")

                if self.inst in ITYPE:
                    if current_loop == 2: tokens.append(Token(TT_REGA, self.current_char))
                    elif current_loop == 3: tokens.append(Token(TT_REGB, self.current_char))
                    elif current_loop == 4:
                        if not(self.current_char.isnumeric()): 
                            self.symbolic = True
                        tokens.append(Token(TT_OFSET, self.current_char))
                        self.not_comment = False
                    else : print("error")

                if self.inst in JTYPE:
                    if current_loop == 2: tokens.append(Token(TT_REGA, self.current_char))
                    elif current_loop == 3: 
                        tokens.append(Token(TT_REGB, self.current_char))
                        tokens.append(Token(TT_NON))
                        #current_loop += 1
                        self.not_comment = False
                    else : print("error")

                if self.inst in OTYPE:
                    if current_loop == 2: 
                        tokens.append(Token(TT_NON))
                        tokens.append(Token(TT_NON))
                        tokens.append(Token(TT_NON))
                        if self.current_char != None: comment += self.current_char + " "
                        #current_loop += 2
                        self.not_comment = False
                    else: 
                        print("error")
                
                if self.inst in SPTYPE:
                    if current_loop == 2: 
                        tokens.append(Token(TT_REGA, self.current_char))
                        tokens.append(Token(TT_NON))
                        tokens.append(Token(TT_NON))
                        self.not_comment = False
                    else : print("error")
                    
                current_loop += 1
                self.advance()

            elif not(self.not_comment):  # check is comment.
                if self.current_char != None:
                    comment += self.current_char + " "
                    self.advance()
                current_loop += 1

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")     

            #print(self.current_char)      

        if not comment: tokens.append(Token(TT_NON))
        else: tokens.append(Token(TT_COMNT, comment))
        
        return tokens, None
        
""" 
    RUN
"""
def run(fn, text, index):
    lexer = Lexer(fn, text, index)
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

# QUESTION #
"""
    1)ตอนใส่ค่าจะเหมือนrisc-vทั่วไปหรือตามตัวอย่าง
    2)๋jalr ในj-typeต่างจากjalr ในi-typeไหม
"""

# NOTE #
"""
    1)อาจจะต้องเปลี่ยนformatตามจาร
        -jalr
        -halt, noop
"""