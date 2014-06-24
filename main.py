import translator
import interpreter

def main():
    import sys
    script_name = sys.argv[0]
    file_name = sys.argv[1]

    try:
        inp = open(script_name, "r")
    except IndexError:
        interpreter.run_interactive()
    except IOError:
        print(file_name, "cannot be opened.")
    else:
        exec( translator.translate(inp) )

if __name__ == "__main__":
    main()