import math
from decimal import Decimal

class Expression:

    def __init__(self,value = None):
        self.value = value

    def get_information(self) -> str:
        return 'Value: '+str(self.value)
    
    def get_type(self):
        return str(type(self))
    
    def evaluate(self,env:dict) -> object:
        return self.value
    
class ExpressionName(Expression):
    def __init__(self,name:str):
        super().__init__()
        self.name = name
    
    def get_information(self) -> str:
        return 'Name: '+self.name
    
    def evaluate(self, env: dict) -> object:
        try:
            return env[self.name]
        except:
            return 'Name {} not defined'.format(self.name)

    
#Simple expressions
class ExpressionPrefix(Expression):
    def __init__(self, operator: str,right_expression: Expression):
        super().__init__()

        self.operator = operator
        self.right = right_expression
    
    def get_information(self) -> str:
        return 'Prefix operator: {}. Expression: {}'.format(self.operator,self.right.get_information())
    
    def evaluate(self, env: dict) -> object:
        value = self.right.evaluate(env=env)

        match self.operator:
            case '~':
                return not value

            case '-':
                return - value

            case _:
                return 'Unknown operator '+self.operator
    
class ExpressionInfix(ExpressionPrefix):
    def __init__(self, operator: str,letf_expression: Expression,right_expression: Expression):
        super().__init__(operator=operator,right_expression=right_expression)

        self.left = letf_expression

    def get_information(self) -> str:
        return 'Infix operator: {}. Left: {}. Right: {}'.format(self.operator,self.left.get_information(),self.right.get_information())
    
    def evaluate(self, env: dict) -> object:
        left = self.left.evaluate(env=env)
        right = self.right.evaluate(env = env)

        if type(left) == str:
            return left
        
        if type(right) == str:
            return right

        match self.operator:
            case 'and':
                return left and right
            case 'or':
                return left or right
            case 'xor':
                return left != right
            case 'in':
                return left in right
            case '=':
                return left == right
            case 'log':
                return math.log(right,left)
            case _:
                return eval('Decimal(left) {} Decimal(right)'.format(self.operator))
    
class ExpressionPosfix(Expression):
    def __init__(self, operator: str, left_expression: Expression):
        super().__init__()

        self.operator = operator
        self.left = left_expression

    def get_information(self) -> str:
        return 'Posfix operator: {}. Expression: {}'.format(self.operator,self.left.get_information())
    
    def evaluate(self, env: dict) -> object:
        if self.operator == '!':
            expression = self.left.evaluate(env=env)
            return math.factorial(int(expression))
        else:
            print('ue')
    

# expressions complex
class ExpressionIf(Expression):
    def __init__(self,condition: Expression, afirmative: Expression, negative=Expression('Void')):
        super().__init__()

        self.condition = condition
        self.afirmative = afirmative
        self.negative = negative

    def get_information(self) -> str:
        return 'Condition: {}. Afirmative case: {}. Negative case: {}'.format(self.condition.get_information(),
                                                                              self.afirmative.get_information(),
                                                                              self.negative.get_information())
    
    def evaluate(self, env: dict) -> object:
        condition = self.condition.evaluate(env=env)

        if (condition != False and not condition is None):
            return self.afirmative.evaluate(env=env)
        else:
            return self.negative.evaluate(env= env)

class ExpressionFunction(Expression):
    def __init__(self, parametrs: list,expression: Expression):
        super().__init__()
        self.parametrs = parametrs
        self.expression = expression

    def get_information(self) -> str:
        return 'Parameters: {}. Expression: {}'.format(self.parametrs,self.expression.get_information())
    
    def evaluate(self, env: dict) -> object:
        return self
    
class CallFunction(Expression):
    def __init__(self, function : str,args:list):
        super().__init__()

        self.function = function
        self.args = args
    
    def get_information(self) -> str:
        return 'Calling function {} with arguments {}'.format(self.function.get_information(),self.args)
    
    def evaluate(self, env: dict) -> object:
        func = env.get(self.function.name)

        if func is None:
            print('Name {} not defined'.format(self.function.name))
            return None

        new_env = env.copy()

        for i in func.parametrs:
            new_env[i] = self.args.pop(0).evaluate(env)

        return func.expression.evaluate(new_env)

    
class ExpressionConjunt(Expression):
    def __init__(self,element:str, rule:Expression = None,elements:list = []):
        super().__init__()

        self.element_name = element
        self.elements = elements
        self.__elements_evaluate:list = None
        self.rule = rule

    def get_information(self) -> str:
        return 'Conjunt. Rule: '+self.rule.get_information()
    
    def __contains__(self,other) -> object:
        if self.rule is None:
            return other in self.elements
        
        new_env = {self.element_name: other}
        return self.rule.evaluate(new_env)
    
    def evaluate(self, env: dict) -> object:
        if self.rule is None:
            if self.__elements_evaluate is None:
                self.__elements_evaluate = []

                for i in self.elements:
                    self.__elements_evaluate.append(i.evaluate(env))

            return self.__elements_evaluate
        return self

class ExpressionVoidConjunt(ExpressionConjunt):
    def __init__(self,):
        super().__init__(element='x', rule=Expression(value=False))