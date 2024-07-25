import lexer.lexer as lex
from lexer.tokens import TypeTokens as tt
import parsing.tree.expressions as exp
import parsing.tree.instructions as inst

prioritys = {
    tt.AND: 1,
    tt.OR: 1,
    tt.XOR: 1,
    tt.EQUAL: 2,
    tt.DIFF: 2,
    tt.IN: 2,
    tt.MINORQ: 2,
    tt.BIGGERQ: 2,
    tt.MINOREQUAL: 2,
    tt.BIGGEREQUAL: 2,
    tt.ADD: 3,
    tt.SUB: 3,
    tt.MUL: 4,
    tt.DIV: 4,
    tt.MOD: 4,
    tt.POW: 5,
    tt.NOT: 6,
    tt.LPAREN: 7,
}

class Parsing:
    def __init__(self,lexer = None,text = None):
        self.lexer = None
        if lexer is None:
            self.lexer = lex.Lexer(text=text)
        else:
            self.lexer = lexer

        self.next_token = self.lexer.next_token()
        self.cur_token = None
        self._get_token()

        self._prefix_fn = {}
        self._posfix_fn = {}
        self._infix_fn = {}

        self.__register_prefix()
        self.__register_posfix()
        self.__register_infix()

    def __register_prefix(self) -> None:
        self._prefix_fn[tt.NUMBER] = self.__parse_number
        self._prefix_fn[tt.TRUE] = self.__parse_bool
        self._prefix_fn[tt.FALSE] = self.__parse_bool
        self._prefix_fn[tt.NAME] = self.__parse_name
        self._prefix_fn[tt.NOT] = self.__parse_prefix
        self._prefix_fn[tt.SUB] = self.__parse_prefix
        self._prefix_fn[tt.LPAREN] = self.__parse_group_expression
        self._prefix_fn[tt.LBRACE] = self.__parse_conjunt_expression
        self._prefix_fn[tt.LBRACKET] = self.__parse_conjuntlist
        self._prefix_fn[tt.IF] = self.__parse_if_expression
        self._prefix_fn[tt.LOG] = self.__parse_log_expression

    def __register_posfix(self) -> None:
        self._posfix_fn[tt.FACTORIAL] = self.__parse_posfix

    def __register_infix(self) -> None:
        self._infix_fn[tt.ADD] = self.__parse_infix
        self._infix_fn[tt.SUB] = self.__parse_infix
        self._infix_fn[tt.MUL] = self.__parse_infix
        self._infix_fn[tt.DIV] = self.__parse_infix
        self._infix_fn[tt.MOD] = self.__parse_infix
        self._infix_fn[tt.AND] = self.__parse_infix
        self._infix_fn[tt.OR] = self.__parse_infix
        self._infix_fn[tt.XOR] = self.__parse_infix
        self._infix_fn[tt.POW] = self.__parse_infix
        self._infix_fn[tt.IN] = self.__parse_infix
        self._infix_fn[tt.MINORQ] = self.__parse_infix
        self._infix_fn[tt.BIGGERQ] = self.__parse_infix
        self._infix_fn[tt.MINOREQUAL] = self.__parse_infix
        self._infix_fn[tt.BIGGEREQUAL] = self.__parse_infix
        self._infix_fn[tt.EQUAL] = self.__parse_infix
        self._infix_fn[tt.DIFF] = self.__parse_infix
        self._infix_fn[tt.LPAREN] = self.__parse_callfunction

    def _get_token(self):
        self.cur_token = self.next_token
        self.next_token = self.lexer.next_token()

    def _expect_token(self, type : tt) -> bool:
        if self.next_token.type == type:
            self._get_token()
            return True
        
        return False
    
    def _get_priority(self,token:tt) -> int:
        priority = prioritys.get(token)
        if priority is None:
            return 0
        
        return priority

    def _parse_expression(self,priority:int) -> exp.Expression:
        parse_prefix = self._prefix_fn.get(self.cur_token.type)

        if parse_prefix is None:
            print('Unknown expression {}'.format(self.cur_token.type))
            return None
        
        expression = parse_prefix()

        parse_posfix = self._posfix_fn.get(self.next_token.type)

        if not parse_posfix is None:
            self._get_token()
            expression = parse_posfix(expression)

        while priority < self._get_priority(self.next_token.type):
            parse_infix = self._infix_fn.get(self.next_token.type)
            if parse_infix is None:
                print('Unknown operation '+self.next_token.type)
                return expression
            
            self._get_token()
            
            expression = parse_infix(expression)

            if expression is None:
                return None
        
        return expression
            

    def _parse_instruction(self) -> inst.Instruction:
        expression = self._parse_expression(priority=0)
        if expression is None:
            return None
        
        return inst.Instruction(expression=expression)

    def __parse_let_function(self) -> inst.LetInstruction:
        if not self._expect_token(tt.NAME):
            print('Defina um nome para sua função')
            return None
        
        name = self.cur_token.value

        if not self._expect_token(tt.LPAREN):
            return None

        list_param = []

        while self.next_token.type != tt.RPAREN:
            if not self._expect_token(tt.NAME):
                return None
            
            list_param.append(self.cur_token.value)

            if self.next_token.type == tt.COMMA:
                self._get_token()

        self._get_token()
        if not self._expect_token(tt.ARROW):
            return None
        
        self._get_token()
        expression = self._parse_expression(priority=0)
        if expression is None:
            return None
            
        return inst.LetInstruction(name=name,expression = exp.ExpressionFunction(parametrs=list_param,expression=expression))


    def __parse_let_var(self,name:str) -> inst.LetInstruction:
        self._get_token()
        self._get_token()

        expression = self._parse_expression(priority=0)

        if expression == None:
            return None
        
        return inst.LetInstruction(name=name,expression=expression)

    def parsing(self) -> inst.Instruction:
        match self.cur_token.type:
            case tt.FUNCTION:
                return self.__parse_let_function()
            
            case tt.NAME:
                if self.next_token.type == tt.COLON:

                    return self.__parse_let_var(self.cur_token.value)
                else:
                    return self._parse_instruction()
                
            case _:
                return self._parse_instruction()
            
    def __parse_number(self) -> exp.Expression:
        number = exp.Expression(value= float(self.cur_token.value))
        if self.next_token.type == tt.NAME:
            self._get_token()
            variable = self.__parse_name()
            return exp.ExpressionInfix(operator=tt.MUL,letf_expression=number,right_expression=variable)

        return number
    
    def __parse_name(self) -> exp.ExpressionName:
        return exp.ExpressionName(name= self.cur_token.value)
    
    def __parse_bool(self) -> exp.Expression:

        if self.cur_token.type == tt.TRUE:
            return exp.Expression(value=True)
        elif self.cur_token.type == tt.FALSE:
            return exp.Expression(value=False)
        else:
            print('ue')
            return None
    
    def __parse_prefix(self) -> exp.ExpressionPrefix:
        operator = self.cur_token.type

        self._get_token()
        right = self._parse_expression(priority=6)

        if right is None:
            return None
        
        return exp.ExpressionPrefix(operator=operator,right_expression=right)
    
    def __parse_infix(self,left:exp.Expression) -> exp.ExpressionInfix:
        operator = self.cur_token.type
        priority = self._get_priority(operator)

        self._get_token()
        right = self._parse_expression(priority=priority)

        if right is None:
            return None
        
        return exp.ExpressionInfix(operator=operator,letf_expression=left,right_expression=right)
    
    def __parse_posfix(self,left:exp.Expression) -> exp.ExpressionPosfix:
        return exp.ExpressionPosfix(operator=self.cur_token.type,left_expression=left)
    
    def __parse_group_expression(self) -> exp.Expression:
        self._get_token()
        expression = self._parse_expression(0)

        if self._expect_token(tt.RPAREN):
            return expression
        
        print('I need you to close the right parenteses')
        return None

    
    def __parse_if_expression(self) -> exp.ExpressionIf:
        self._get_token()

        condition = self._parse_expression(0)

        if condition is None:
            return None

        if self._expect_token(tt.THEN):
            self._get_token()

            afirmative = self._parse_expression(0)

            if afirmative is None:
                return None
            
            
            if self.next_token.type == tt.ELSE:
                self._get_token()
                self._get_token()
                negative = self._parse_expression(0)

                return exp.ExpressionIf(condition=condition,afirmative=afirmative,negative=negative)
            
            return exp.ExpressionIf(condition=condition,afirmative=afirmative)


        print('Was waiting for '+tt.THEN)
        return None
    
    def __parse_log_expression(self) -> exp.ExpressionInfix:
        operator = self.cur_token.type
        self._get_token()

        exp_base = self._parse_expression(0)
        self._get_token()
        exp_exponent = self._parse_expression(0)

        if exp_base is None or exp_exponent is None:
            return None
        
        return exp.ExpressionInfix(operator=operator,letf_expression=exp_base,right_expression=exp_exponent)
    
    def __parse_callfunction(self,left:exp.Expression) -> exp.CallFunction:
        arguments = []

        while True:
            self._get_token()
            expression= self._parse_expression(0)
            if expression is None:
                return None
            
            arguments.append(expression)

            if self.next_token.type == tt.COMMA:
                self._get_token()
                continue
            elif self.next_token.type == tt.RPAREN:
                self._get_token()
                break
            else:
                print('I need you to close function call with right parentheses')
                return None
            
        return exp.CallFunction(function=left,args=arguments)
    
    def __parse_conjunt_expression(self) -> exp.ExpressionConjunt:
        if not self._expect_token(tt.NAME):
            print('Define one controll variable')
            return None
        
        name = self.cur_token.value

        if not self._expect_token(tt.VERTICALBAR):
            print('Separe the controll variable of the rule with vertical bar')
            return None
        
        self._get_token()

        rule = self._parse_expression(0)

        if rule is None or not self._expect_token(tt.RBRACE):

            print('I need you to close conjunt expressions with right brace.')
            return None
        
        return exp.ExpressionConjunt(element=name,rule=rule)
    
    def __parse_conjuntlist(self) -> exp.ExpressionConjunt:
        if self.next_token.type == tt.RBRACKET:
            return exp.ExpressionVoidConjunt()
        
        elements:list = []
        
        while True:
            self._get_token()

            expression = self._parse_expression(0)

            if expression is None:
                return None
            
            elements.append(expression)

            if self.next_token.type == tt.COMMA:
                self._get_token()
                continue
            elif self.next_token.type == tt.RBRACKET:
                break
            else:
                print('I need you to close the list elements with right bracket')
                return None
            
        return exp.ExpressionConjunt(element='x',elements=elements)