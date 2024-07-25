import lexer.tokens as tk

letter_to_tokens = {
    '+': tk.TypeTokens.ADD,
    '-': tk.TypeTokens.SUB,
    '*': tk.TypeTokens.MUL,
    '/': tk.TypeTokens.DIV,
    '%': tk.TypeTokens.MOD,
    '<': tk.TypeTokens.MINORQ,
    '>': tk.TypeTokens.BIGGERQ,
    '=': tk.TypeTokens.EQUAL,
    '!': tk.TypeTokens.FACTORIAL,
    '~': tk.TypeTokens.NOT,
    '|': tk.TypeTokens.VERTICALBAR,
    ',': tk.TypeTokens.COMMA,
    ';': tk.TypeTokens.SEMICOLON,
    ':': tk.TypeTokens.COLON,
    '(': tk.TypeTokens.LPAREN,
    ')': tk.TypeTokens.RPAREN,
    '[': tk.TypeTokens.LBRACKET,
    ']': tk.TypeTokens.RBRACKET,
    '{': tk.TypeTokens.LBRACE,
    '}': tk.TypeTokens.RBRACE,
    '\n': tk.TypeTokens.NLINE
}

keywords = {
    'and': tk.TypeTokens.AND,
    'or': tk.TypeTokens.OR,
    'xor': tk.TypeTokens.XOR,
    'true': tk.TypeTokens.TRUE,
    'false': tk.TypeTokens.FALSE,
    'log': tk.TypeTokens.LOG,
    'in': tk.TypeTokens.IN,
    'if': tk.TypeTokens.IF,
    'then': tk.TypeTokens.THEN,
    'else': tk.TypeTokens.ELSE,
    'fn': tk.TypeTokens.FUNCTION,
}

class Lexer:
    def __init__(self,text: str):
        self.text = text
        self.cur_letter = ''
        self.next_letter = ''
        self.pos_letter = 0

        self._read_letter()
        self._read_letter()
    
    def _read_letter(self):
        self.cur_letter = self.next_letter

        try:
            self.next_letter = self.text[self.pos_letter]
        except:
            self.next_letter = 'END'
        self.pos_letter += 1

    def _ignore_spaces(self):
        while self.cur_letter == ' ' or self.cur_letter == '\t':
            self._read_letter()

    def _is_number(self,letter: str) -> bool:
        if letter in '0123456789':
            return True
        return False
    
    def _is_letter(self,letter: str) -> bool:
        if letter in 'abcdefghijklmnopqrstuvwxyz_':
            return True
        
        if letter.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return True
        
        return False

    def _get_token(self) -> tk.Token:
        try:
            return tk.Token(letter_to_tokens[self.cur_letter])
        except:
            return tk.Token(tk.TypeTokens.UNKNOWN,self.cur_letter)
    
    def _get_token_name(self) -> tk.Token:
        name = self.cur_letter
        while self._is_letter(self.next_letter) or self._is_number(self.next_letter):
            self._read_letter()
            name += self.cur_letter

        type_word = keywords.get(name)

        if type_word is None:

            return tk.Token(tk.TypeTokens.NAME,name)
        else:
            return tk.Token(type_word)
    
    def _get_token_number(self) -> tk.Token:
        number = self.cur_letter
        while self._is_number(self.next_letter) or self.next_letter == '.':
            if self.next_letter == '.' and '.' in number:
                break
            self._read_letter()
            number += self.cur_letter

        return tk.Token(tk.TypeTokens.NUMBER,number)

    def next_token(self) -> tk.Token:
        token = None
        self._ignore_spaces()

        match self.cur_letter:
            case '<':
                if self.next_letter == '=':
                    token = tk.Token(tk.TypeTokens.MINOREQUAL)
                    self._read_letter()
                else:
                    token =  self._get_token()
            
            case '>':
                if self.next_letter == '=':
                    token = tk.Token(tk.TypeTokens.BIGGEREQUAL)
                    self._read_letter()
                
                else:
                    token = self._get_token()

            case '-':
                if self.next_letter == '>':
                    token = tk.Token(tk.TypeTokens.ARROW)
                    self._read_letter()
                else:
                    token = self._get_token()

            case '*':
                if self.next_letter == '*':
                    token = tk.Token(tk.TypeTokens.POW)
                    self._read_letter()
                else:
                    token = self._get_token()
            
            case '~':
                if self.next_letter == '=':
                    token = tk.Token(tk.TypeTokens.DIFF)
                    self._read_letter()
                else:
                    token = self._get_token()
            
            case 'END':
                return tk.Token(tk.TypeTokens.END)

            case _:

                if self._is_letter(self.cur_letter):
                    token = self._get_token_name()

                elif self._is_number(self.cur_letter):
                    token = self._get_token_number()

                else:
                    token = self._get_token()


        self._read_letter()

        return token