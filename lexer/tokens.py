from enum import StrEnum

class TypeTokens(StrEnum):
    #operations maths
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    POW = '**'
    IN = 'in'

    #operations comparison
    MINORQ = '<'
    BIGGERQ = '>'
    MINOREQUAL = '<='
    BIGGEREQUAL = '>='
    EQUAL = '='
    DIFF = '~='

    #operations logics
    AND = 'and'
    OR = 'or'
    NOT = '~'
    XOR = 'xor'

    #operations prefix
    VERTICALBAR = '|'

    #operations posfix
    FACTORIAL = '!'

    #logic values
    TRUE = 'true'
    FALSE = 'false'

    #others operations
    LOG = 'log'
    ARROW = '->'
    COLON = ':'

    #delimiters
    END = 'END'
    NLINE = '\n'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    LBRACKET = '['
    RBRACKET = ']'
    COMMA = ','
    SEMICOLON = ';'

    #conditional
    IF = 'if'
    THEN = 'then'
    ELSE = 'else'

    #data types:
    NUMBER = 'NUMBER'
    NAME = 'NAME'
    FUNCTION = 'fn'

    UNKNOWN = 'UNK'


class Token:
    def __init__(self,type: TypeTokens,value = ''):
        self.type = type
        self.value = value