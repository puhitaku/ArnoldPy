class Runnables(object):
    def __init__(self):
        raise NotImplementedError

    def get_parsed_structure(self):
        raise NotImplementedError

class Block(Runnables):
    def __init__(self):
        self.child_run = []

    def add_child(self, child):
        self.child_run.append(child)

class Statement(Runnables):
    def __init__(self):
        pass

class Main(Block):
    def __init__(self, child=[]):
        super().__init__()
        self.child_run = child

    def get_parsed_structure(self):
        s = ""
        for i in self.child_run:
            if type(i) in [type(If()), type(IfElse()), type(While())]:
                s += i.get_parsed_structure(nest_lv=1)
            else:
                s += "".join(i.get_parsed_structure(), "\n")
        return s

class If(Block):
    def __init__(self, value, statements):
        super().__init__()
        self.value = value
        self.child_run = statements

    def get_parsed_structure(self, nest_lv=0):
        s = "".join("    " * nest_lv, "if ", self.value, ":\n")
        for i in self.child_run:
            if type(i) in [type(If()), type(IfElse()), type(While())]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join("    " * (nest_lv+1), i.get_parsed_structure(), "\n")
        return s

class IfElse(Block):
    def __init__(self, value, statements, statements_e):
        super().__init__()
        self.value = value
        self.child_run = statements
        self.child_run_e = statements_e

    def get_parsed_structure(self, nest_lv=0):
        s = "".join("    " * nest_lv, "if ", self.value, ":\n")
        for i in self.child_run:
            if type(i) in [type(If()), type(IfElse()), type(While())]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join("    " * (nest_lv+1), i.get_parsed_structure(), "\n")

        s += "".join("    " * nest_lv, "else:\n")
        for i in self.child_run_e:
            if type(i) in [type(If()), type(IfElse()), type(While())]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join("    " * (nest_lv+1), i.get_parsed_structure(), "\n")
        return s

class While(Block):
    def __init__(self, value, statements):
        super().__init__()
        self.value = value
        self.child_run = statements

    def get_parsed_structure(self, nest_lv=0):
        s = "".join("    " * nest_lv, "while ", self.value, ":\n")
        for i in self.child_run:
            if type(i) in [type(If()), type(IfElse()), type(While())]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join("    " * (nest_lv+1), i.get_parsed_structure(), "\n")
        return s

class Print(Statement):
    def __init__(self, string):
        self.string = string

    def get_parsed_structure(self):
        return "".join(["print(\"", self.string, "\")"])

class DeclaringVariable(Statement):
    def __init__(self, name, value):
        self.name, self.value = name, value

    def get_parsed_structure(self):
        return "".join([self.name, " = ", self.value])

class EvaluatingExpression(Statement):
    def __init__(self, operands, operations):
        self.operands = operands
        self.operations = operations

        self.operations.insert(0, "")
        #To avoid calculate first operand with nothing

    def get_parsed_structure(self):
        s = ""
        for (i, j) in zip(self.operations, self.operands):
            s = "".join(["(", s, i, j, ")"])
        return s

class AssigningValue(Statement):
    def __init__(self, name, operands, operations):
        self.name = name
        self.exp = EvaluatingExpression(operands, operations)

    def get_parsed_structure(self):
        s = self.exp.get_parsed_structure()
        return "".join([self.name, " = ", s])