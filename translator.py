import reserved_words as rword

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
    def __init__(self):
        super().__init__()
        self.child_run = []
        self.If, self.IfElse, self.While = If("", []), IfElse("", [], []), While("", [])

    def get_parsed_structure(self):
        s = ""
        for i in self.child_run:
            if type(i) in [type(self.If), type(self.IfElse), type(self.While)]:
                s += i.get_parsed_structure(nest_lv=1)
            else:
                s += "".join([i.get_parsed_structure(), "\n"])
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
        return "".join([self.name, " = ", str(self.value)])

class EvaluatingExpression(Statement):
    def __init__(self, args, operations):
        self.args = args
        self.operations = operations

        self.operations.insert(0, "")
        #To avoid calculate first arg with nothing

    def get_parsed_structure(self):
        s = ""
        for (i, j) in zip(self.operations, self.args):
            s = "".join(["(", s, i, j, ")"])
        return s

class AssigningValue(Statement):
    def __init__(self, name, args, operations):
        self.name = name
        self.exp = EvaluatingExpression(args, operations)

    def get_parsed_structure(self):
        s = self.exp.get_parsed_structure()
        return "".join([self.name, " = ", s])

def GetOperation(l):
    return "".join( l.split()[:-1] )

def GetArgument(l):
    return code[pc].split()[-1]

def GetEndOfBlock(code, end_op):
    for i in code:
        if end_op in i:
            return i
    else:
        return -1

def GetArithmeticOpList(code, operator):
    op_list = []
    arg_list = []
    for i in code:
        op = " ".join(i.split()[:-1])
        arg = i.split()[-1]

        if op in operator:
            arg_list.append(arg)
            op_list.append(operator[op])
    return op_list, arg_list

def Translate(inp):
    code = inp.readlines()
    w = rword.ReservedWords()
    stack = []
    pc = 0
    WTFException = rword.WhatTheFuckDidIDoWrong
    while True:
        l   = code[pc]
        op  = GetOperation(l)
        arg = GetArgument(l)

        if w.word["Main"] == op:
            if stack == []:
                stack.append(pc)
            else:
               raise WTFException(pc+1, "attempted to begin Main method in another method")

        if w.word["Main_end"] == op:
            if len(stack) == 1:
                sys.exit()
            else:
                raise WTFException(pc+1, "unexpected end of Main")

        if w.word["If"] == op:
            b = code[pc:pc + GetEndOfBlock(code[pc:], w.word["If_end"])]
            var = arg
            op_list = GetArithmeticOpList(b, w.operator)
            arg_list = GetArithmeticArgList(b, w.operator)


        if w.word["While"] == op:
            pass
