import sys

import translator as tr
#import interpreter

def main():
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
        exec( tr.Translate(inp) )

if __name__ == "__main__":
    main()