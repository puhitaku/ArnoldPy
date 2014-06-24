def run(inp):
    import sys

    blocks = {
        "Main":      "IT'S SHOWTIME",
        "Main_end":  "YOU HAVE BEEN TERMINATED",
        "If":        "BECAUSE I'M GOING TO SAY PLEASE",
        "Else":      "BULLSHIT",
        "If_end":    "YOU HAVE NO RESPECT FOR LOGIC",
        "While":     "STICK AROUND",
        "While_end": "CHILL"
    }

    statements = {
        "Print":          "TALK TO THE HAND",
        "DecVar_name":    "HEY CHRISTMAS TREE",
        "DecVar_value":   "YOU SET US UP",
        "AssignVar_name": "GET TO THE CHOPPER",
        "AssignVar_opr":  "HERE IS MY INVITATION",
        "AssignVar_end":  "ENOUGH TALK",
        "Plus":           "GET UP",
        "Minus":          "GET DOWN",
        "Multiply":       "YOU'RE FIRED",
        "Divide":         "HE HAD TO SPLIT",
        "EqualTo":        "YOU ARE NOT YOU YOU ARE ME",
        "GreaterThan":    "LET OFF SOME STEAM BENNET",
        "Or":             "CONSIDER THAT A DIVORCE",
        "And":            "KNOCK KNOCK"
    }

    code = inp.readlines()
    pc = 0
    stack = []

    while(pc < len(code)):
        try:
            line = code[pc]
        except IndexError:
            print("Unexpected EOF: Missing \"YOU HAVE BEEN TERMINATED\"? ")
            sys.exit()

        opr = set(line)

        if blocks["Main"] in line:
            stack.append(pc)

        if blocks["Main_end"] in line:
            stack.pop()
            if stack != []:
                print("Unexpected end of Main method.")
                sys.exit()

        if blocks["If"] in line:
            stack.append(pc)
            exp = 