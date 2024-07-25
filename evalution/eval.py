from parsing.tree.instructions import Instruction
from parsing.tree.expressions import ExpressionFunction
import evalution.functions as fn
import math

environment = {
    'pi': math.pi,
    'e': math.e,
    'sum': ExpressionFunction(parametrs=['init','step','max'],expression=fn.FunctionSum()),
    'abs': ExpressionFunction(parametrs=['value'],expression=fn.FunctionAbs()),
    'rad': ExpressionFunction(parametrs=['value'],expression=fn.FunctionToRad()),
    'sin': ExpressionFunction(parametrs=['value'],expression=fn.FunctionSin()),
    'cos': ExpressionFunction(parametrs=['value'],expression=fn.FunctionCos()),
    'tan': ExpressionFunction(parametrs=['value'],expression=fn.FunctionTan()),
    'invert': ExpressionFunction(parametrs=['value'],expression=fn.FunctionInvert()),
    'sqrt': ExpressionFunction(parametrs=['value'],expression=fn.FunctionSquareRoot()),
    'root': ExpressionFunction(parametrs=['base','exponent'],expression=fn.FunctionRoot),
    'sequation1': ExpressionFunction(parametrs=['a','b'],expression=fn.FunctionSimpleEquationSolving()),
    'sequation2': ExpressionFunction(parametrs=['a','b','c'],expression=fn.FunctionQuadraticEquationSolving())
}

def Eval(instruction:Instruction) -> object:
    result = instruction.execute(environment)

    print(result)