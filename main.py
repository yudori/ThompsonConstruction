from expression import *

if __name__ == "__main__":
    while True:
        infix = raw_input("\n>>Enter regular expression: ")
        postfix = re_to_postfix(infix)
        print postfix
        postfix_to_nfa(postfix)