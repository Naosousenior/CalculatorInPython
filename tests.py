from lexer.lexer import Lexer
from lexer.tokens import TypeTokens
import parsing.tree.expressions as expr
from parsing.parsing import Parsing
from evalution.eval import Eval

def tests_tokens(text) -> str:
    lexer = Lexer(text)
    token = lexer.next_token()
    while token.type != TypeTokens.END:
        print(token.type.name,token.value+',')
        token = lexer.next_token()

def test_expression():
    expression1 = expr.Expression(value = 1)
    expression2 = expr.ExpressionPrefix(operator='-',right_expression=expr.Expression(5))
    expression3 = expr.ExpressionPrefix(operator='-',right_expression=expression2)
    expression4 = expr.ExpressionIf(condition=expr.Expression(True),afirmative=expression1)

    print(expression1.get_information(),expression1.get_type())
    print(expression2.get_information(),expression2.get_type())
    print(expression3.get_information(),expression3.get_type())
    print(expression4.get_information(),expression4.get_type())

def test_parsing(command: str):
    parser = Parsing(lexer=Lexer(command))

    instruction = parser.parsing()

    print(instruction.expression.get_information())

def test_evaluate(command: str):
    parser = Parsing(lexer=Lexer(command))
    instruction = parser.parsing()
    Eval(instruction=instruction)