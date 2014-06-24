def run(inp):
    import sys
    import reserved_words as rword

    w = rword.ReservedWords()
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

        if w.word["Main"] in line:
            stack.append(pc)

        if w.word["Main_end"] in line:
            stack.pop()
            if stack != []:
                print("Unexpected end of Main method.")
                sys.exit()

        if w.word["If"] in line:
            stack.append(pc)
            exp = 