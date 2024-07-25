from parsing.tree.expressions import Expression

class Instruction:
    def __init__(self,expression:Expression) -> None:
        self.expression = expression

    def execute(self,env:dict) -> object:
        return self.expression.evaluate(env=env)

class LetInstruction(Instruction):
    def __init__(self, name:str,expression:Expression) -> None:
        super().__init__(expression)

        self.name = name

    def execute(self,env: dict) -> object:

        value = self.expression.evaluate(env=env)

        if value is str:
            print(value)
            return None
        
        env[self.name] = self.expression.evaluate(env=env)

        return 'Name {} defined with value {}'.format(self.name,value)