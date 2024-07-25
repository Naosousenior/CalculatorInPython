from parsing.tree.expressions import Expression, ExpressionConjunt
from decimal import Decimal
import math

class FunctionAbs(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        num = env['value']

        if num < 0:
            return -num
        
        return num
    
class FunctionSum(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        init = int(env['init'])-1
        step = int(env['step'])
        max = int(env['max'])

        qtt = (max-init)//step
        final_true = init +(step + qtt)

        return (init +final_true)*qtt/2
    
class FunctionToRad(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        value = env['value']

        return math.radians(value)
    
class FunctionSin(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        value = env['value']

        return math.sin(value)
    
class FunctionCos(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        value = env['value']

        return math.cos(value)
    
class FunctionTan(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        value = env['value']

        return math.tan(value)
    
class FunctionInvert(Expression):
    def __init__(self,):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        value = env['value']

        return 1/value
    
class FunctionSquareRoot(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        value = env['value']

        return Decimal(value) ** Decimal(0.5)
    
class FunctionRoot(Expression):
    def __init__(self,):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        base = env['base']
        exponent = env['exponent']

        return Decimal(base) ** (Decimal(1)/Decimal(exponent))
    
class FunctionSimpleEquationSolving(Expression):
    def __init__(self, value=None):
        super().__init__(value)

    def evaluate(self, env: dict) -> object:
        a = Decimal(env['a'])
        b = Decimal(env['b'])

        if a == 0:
            print('Division by zero is impossible')
            return None
        
        return (-b)/a
    
class FunctionQuadraticEquationSolving(Expression):
    def __init__(self):
        super().__init__()

    def evaluate(self, env: dict) -> object:
        a = Decimal(env['a'])
        b = Decimal(env['b'])
        c = Decimal(env['c'])

        delta = b**2-4*a*c

        if delta < 0:
            print('I no work with complex numbers')
            return None
        
        x1 = (-b+math.sqrt(delta))/2*a
        x2 = (-b-math.sqrt(delta))/2*a

        return ExpressionConjunt(element='x',elements=[x1,x2])