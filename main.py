import sys

import translator as tr
#import interpreter

def main():
    debug = True
    script_name = sys.argv[0]

    try:
        file_name = sys.argv[1]
        inp = open(file_name, "r")
    except IndexError:
        pass
        #interpreter.run_interactive()
    except IOError:
        print("Could not open:", file_name)
    else:
        t = tr.Translate(inp, False)

        if debug:
            print("%sTranslated code:\n%s%s" % ("\x1B[33m", "\x1B[39;49m", t))
            print("%s----- begin%s" % ("\x1B[32m", "\x1B[39;49m"))

        exec(t)

        if debug:
            print("%s----- end%s" % ("\x1B[32m", "\x1B[39;49m"))

if __name__ == "__main__":
    main()