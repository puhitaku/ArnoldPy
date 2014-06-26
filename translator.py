import reserved_words as rword

class Runnables(object):
    """Abstract definition of runnable blocks/statements"""
    def __init__(self):
        raise NotImplementedError

    def get_parsed_structure(self):
        raise NotImplementedError

class Block(Runnables):
    """Common constructor and methods that Blocks have"""
    """Main, If and While are included"""
    def __init__(self):
        self.child = []

    def add_child(self, child):
        self.child.append(child)
        return self.child[-1]

class Statement(Runnables):
    """Common definition of Statements (Not longer needed?)"""
    def __init__(self):
        pass

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
        else_flag = False
        s = "".join("    " * nest_lv, "if ", self.value, ":\n")
        for i in self.child:
            if i == "else":
                else_flag = True
                continue
            if type(i) in [type(If()), type(While())]:
                s += i.get_parsed_structure(nest_lv=nest_lv+1)
            else:
                s += "".join("    " * (nest_lv+1), i.get_parsed_structure(), "\n")

        if else_flag:
            s += "".join("    " * nest_lv, "else:\n")
            for i in self.child_e:
                if type(i) in [type(If()), type(While())]:
                    s += i.get_parsed_structure(nest_lv=nest_lv+1)
                else:
                    s += "".join("    " * (nest_lv+1), i.get_parsed_structure(), "\n")
        return s

class While(Block):
    """While block"""
    def __init__(self, exp):
        super().__init__()
        self.value = exp

    def get_parsed_structure(self, nest_lv=0):
        s = "".join(["    " * nest_lv,
                     "while ((type(%s) == type(int())) & (%s == 0)) | ((type(%s) == type(bool())) & (%s == True))"
                     % (self.value, self.value, self.value, self.value),
                     ":\n"])
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
    """Declaration of variables"""
    def __init__(self, name, value):
        self.name, self.value = name, value

    def get_parsed_structure(self):
        return "".join([self.name, " = ", str(self.value)])

class Expression(Statement):
    """Expression recognizer class"""
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
        self.exp = Expression(args, operations)

    def get_parsed_structure(self):
        s = self.exp.get_parsed_structure()
        return "".join([self.name, " = ", s])

def GetOprAndArgs(l):
    r = rword.ReservedWords()
    lsp = set(l.split())
    opr = ""
    for i in r.word.values():
        isp = set(i.split())
        if lsp & isp == isp:
            opr = " ".join( l.split()[:-len(lsp - isp)] )
    if opr == "":
        return l, "<NONE>"
    arg = " ".join( l.split()[len(opr.split()):] )
    return opr, arg

def GetEndOfBlock(code, end_op):
    for i in code:
        if end_op in i:
            return code.index(i)
    else:
        return -1

def GetArithmeticElements(code, operator):
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
    code = code.replace("@NO PROBLEMO", "0")
    code = code.replace("@I LIED", "1")
    return code

def Translate(inp, debug=False):
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
        if pc < len(code) - 1:
            l_   = code[pc+1]
            if l_[-1] == "\n":
                l_ = l_[:-1]
            op_, arg_  = GetOprAndArgs(l_)



        if debug:
            print("l:", l)
            print("op:", op)
            print("arg:", arg)
            print("")

        if w.word["Main"] == l:
            if ptr == None:
                tree = Main()
                ptr = tree
            else:
               raise WTFException(pc+1, "attempted to begin Main method in another method")

        elif w.word["Main_end"] == l:
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
            if type(ptr) == type(If):
                if ptr.has_else() == False:
                    ptr.add_else()
                else:
                    raise WTFException(pc+1, "there is already Else before this")
            else:
                raise WTFException(pc+1, "there is no If before Else")

        elif w.word["While"] == op:
            stack.append(ptr)
            ptr = ptr.add_child(While(arg))

        elif l in [w.word["If_end"], w.word["While_end"]]:
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

            op_list, arg_list = GetArithmeticElements(b, w.operator)
            ptr.add_child(AssigningValue(arg, [arg_] + arg_list, op_list))
            pc += offset

        else:
            raise WTFException(pc+1, "unknown: " + op)

        pc += 1
