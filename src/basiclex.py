# 
# Modified Dartmouth BASIC (1964)
# Original sources: 
# Added bitwise operators 

from ply import *

keywords = (
   'LET', 'READ', 'DATA', 'PRINT', 'GOTO', 'IF', 'THEN', 'FOR', 'NEXT', 'TO', 'STEP',
    'END', 'STOP', 'DEF', 'GOSUB', 'DIM', 'REM', 'RETURN', 'RUN', 'LIST', 'NEW', 'FIFO',
    'AND', 'OR', 'NOT'
)

tokens = keywords + (
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'SEMI', 'INTEGER', 'HEX', 'FLOAT', 'STRING',
    'ID', 'NEWLINE', 'SL', 'SR' , 'BAND', 'BOR', 'BNOT', 'XOR', 'MOD','EQUALSEQUALS',
)

t_ignore = ' \t'


def t_REM(t):
    r'REM .*'
    return t

def t_ID(t):
    r'[A-Z][A-Z0-9]*'
    if t.value in keywords:
        t.type = t.value
    return t

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\*\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'<>'
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_HEX = r'^(0[xX])?[A-Fa-f0-9]+$'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'
t_SL = r'<<'
t_SR = r'>>'
t_BAND = r'&'
t_BOR = r'\|'
t_BNOT = r'~'
t_XOR = r'\^'
t_MOD = r'%'
t_EQUALSEQUALS = r'=='

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(debug=0)
