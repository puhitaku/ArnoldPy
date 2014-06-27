""" ArnoldC -> Python translator
    This file includes abstract model of blocks and statements.

"""

import reserved_words as rword

#Abstract syntax model
#---------------------

class Runnables(object):
    """Abstract definition of runnable blocks/statements"""
    def __init__(self):
        raise NotImplementedError

    def get_parsed_structure(self):
        raise NotImplementedError

class Block(Runnables):
    """Common constructor and methods that Blocks have"""
    """Main, If and While are included."""
    def __init__(self):
        self.child = []

    def add_child(self, child):
        self.child.append(child)
        return self.child[-1]

class Statement(Runnables):
    """Common definition of Statements (Not longer needed?)"""
    def __init__(self):
        pass

#Concrete blocks/statements model
#--------------------------------

class Main(Block):
    """Main method"""
    def __init__(self):
        super().__init__()

    def get_parsed_structure(self):
        s = ""
        for i in self.child:
            if type(i) in [type(If), type(While)]:
                s += i.get_parsed_structure(nest_lv=1)
            else:
                s += "".join([i.get_parsed_structure(), "\n"])

        while (s[-1], s[-2]) == ("\n", "\n") :
            s = s[:-1]
        return s

class If(Block):
    """If block"""
    def __init__(self, exp):
        super().__init__()
        self.value = exp

    def add_else(self):
        self.child.append("else")

    def has_else(self):
        return "else" in self.child

    def get_parsed_structure(self, nest_lv=0):
        s = "".join(["    " * nest_lv, "if %s:\n" % GetEvalExpression(self.value)])

        for i in self.child:
            if i == "else":
                s += "".join(["    " * nest_lv, "else:\n"])
            elif type(i) in [type(If("")), type(While(""))]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join(["    " * (nest_lv+1), i.get_parsed_structure(), "\n"])
        return s

class While(Block):
    """While block"""
    def __init__(self, exp):
        super().__init__()
        self.value = exp

    def get_parsed_structure(self, nest_lv=0):
        s = "".join(["    " * nest_lv, "while %s:\n" % GetEvalExpression(self.value)])
        for i in self.child:
            if type(i) in [type(If("")), type(While(""))]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join(["    " * (nest_lv+1), i.get_parsed_structure(), "\n"])
        return s

class Print(Statement):
    """Print statement"""
    def __init__(self, string):
        self.string = string

    def get_parsed_structure(self):
        return "".join(["print(", self.string, ")"])

class DeclaringVariable(Statement):
    """Variable declaration"""
    def __init__(self, name, value):
        self.name, self.value = name, value

    def get_parsed_structure(self):
        return "".join([self.name, " = ", str(self.value)])

class Expression(Statement):
    """Expression recognizer class"""
    """It inherits Statement class but it's not a statement."""
    """It's used to construct the right side of equation."""
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
    """Value assign statement"""
    """It uses Expression class to get the right side of equation."""
    def __init__(self, name, args, operations):
        self.name = name
        self.exp = Expression(args, operations)

    def get_parsed_structure(self):
        s = self.exp.get_parsed_structure()
        return "".join([self.name, " = ", s])


#Functions for syntax analysis
#-----------------------------

def GetOprAndArgs(l):
    """Extract the list of operations and their arguments from block."""
    r = rword.ReservedWords()
    lsp = set(l.split())
    opr = ""
    for i in r.word.values():
        isp = set(i.split())
        if lsp & isp == isp:
            opr = " ".join( l.split()[:-len(lsp - isp)] )
    if opr == "":
        return " ".join(l.split()), "<NONE>"
    arg = " ".join( l.split()[len(opr.split()):] )
    return opr, arg

def GetEndOfBlock(code, end_op):
    """Get the last line of block."""
    """It returns -1 if it can't find."""
    for i in code:
        if end_op in i:
            return code.index(i)
    else:
        return -1

def GetArithmeticMembers(code, operator):
    """Get members and operators used in equation."""
    op_list = []
    arg_list = []
    for i in code:
        op = " ".join(i.split()[:-1])
        arg = i.split()[-1]

        if op in operator.keys():
            arg_list.append(arg)
            op_list.append(operator[op])
    return op_list, arg_list

def ReplaceMacros(code):
    """Replace macro words."""
    w = rword.ReservedWords()
    code = code.replace(w.word["1"], "1")
    code = code.replace(w.word["0"], "0")
    return code

def GetEvalExpression(value):
    """Generate evaluation formula."""
    """In ArnoldC, 0 means True and other numbers mean False."""
    """To follow ArnoldC's evaluation rule, it's little complicated."""
    return "(%s if type(%s) == type(bool()) else %s > 0)" % tuple([value]*3)


#Main translator function
#------------------------

def Translate(inp, debug=False):
    """Translate the ArnoldC code in Python."""
    code = inp.readlines()
    w = rword.ReservedWords()
    tree = None
    stack = [None]
    ptr = None
    pc = 0

    WTFException = rword.WhatTheFuckDidIDoWrong

    while True:
        #Get a line of program
        try:
            l = code[pc]
        except IndexError:
            raise WTFException(pc+1, "unexpected EOF")
        else:
            if l[-1] == "\n":
                l = l[:-1]
            op, arg   = GetOprAndArgs(l)

        #Remove \n code
        try:
            l_   = code[pc+1]
        except IndexError:
            pass
        else:
            if l_[-1] == "\n":
                l_ = l_[:-1]
            op_, arg_  = GetOprAndArgs(l_)



        if debug:
            print("l:", l)
            print("op:", op)
            print("arg:", arg)
            print("")

            print("l_:", l_)
            print("op_:", op_)
            print("arg_:", arg_)
            print("\n")

        if w.word["Main"] == op:
            if ptr == None:
                tree = Main()
                ptr = tree
            else:
               raise WTFException(pc+1, "attempted to begin Main method in another method")

        elif w.word["Main_end"] == op:
            if type(ptr) == type(Main()):
                out = ReplaceMacros(ptr.get_parsed_structure())
                if debug:
                    print(out)
                return out
            else:
                raise WTFException(pc+1, "unexpected end of Main: " + str(type(ptr)))

        elif w.word["If"] == op:
            stack.append(ptr)
            ptr = ptr.add_child(If(arg))

        elif w.word["Else"] == op:
            if type(ptr) == type(If("")):
                if ptr.has_else() == False:
                    ptr.add_else()
                else:
                    raise WTFException(pc+1, "there is already Else before this")
            else:
                raise WTFException(pc+1, "there is no If before Else:")

        elif w.word["While"] == op:
            stack.append(ptr)
            ptr = ptr.add_child(While(arg))

        elif op in [w.word["If_end"], w.word["While_end"]]:
            ptr = stack.pop()

        elif w.word["Print"] == op:
            ptr.add_child(Print(arg))

        elif (w.word["DecVar"] == op) & (w.word["DecVar_value"] == op_):
            ptr.add_child(DeclaringVariable(arg, arg_))
            pc += 1

        elif (w.word["AssignVar"] == op) & (w.word["AssignVar_opr"] == op_):
            pc += 1
            offset = GetEndOfBlock(code[pc:], w.word["AssignVar_end"])
            b = code[pc:pc + offset]

            op_list, arg_list = GetArithmeticMembers(b, w.operator)
            ptr.add_child(AssigningValue(arg, [arg_] + arg_list, op_list))
            pc += offset

        elif op == "":
            pass

        else:
            raise WTFException(pc+1, "unknown: \"%s\"" % op)

        pc += 1
