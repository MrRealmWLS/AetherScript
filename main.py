import os
import sys

class AetherError():
    def __init__(self, message,type_):
        self.message = message
        self.type = type_
    def raised(self,line):
        print(f"{self.type}: {self.message} on {line}")
class AetherSyntaxError(AetherError):
    def __init__(self, message):
        super().__init__(message,"SyntaxError")
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def Lexer(source_code): 
    chars=list(source_code)
    line = 1
    tokens = []
    statematent = ""
    open_parenthesis = 0
    count = 1
    is_string_open=False
    for char in chars:
        statematent += char
        
        if char == "\n":
            line += 1
            statematent = ""
        elif char == '"':
            if is_string_open == False:
                statematent = ""
                is_string_open = True
            else:
                statematent = statematent[:-1]
                tokens.append({ "type": "STRING", "value": statematent })
                statematent = ""
                is_string_open = False
                
        elif char == "(":
            open_parenthesis += 1
            tokens.append({ "type": "LPAREN", "value": "(" })
            statematent = ""
        elif char == ")":
            open_parenthesis -= 1
            tokens.append({ "type": "RPAREN", "value": ")" })
            statematent = ""
        elif char == ";":
            tokens.append({ "type": "SEMICOLON", "value": ";" })
            statematent = ""

        if statematent == "print":
            tokens.append({ "type": "KEYWORD", "value": "print" })
            statematent = ""

        count+=1
    return tokens
def Parser(tokens):
    pass
def main(file_path):
    source_code = read_file(file_path)
    print(Lexer(source_code))
arguments = sys.argv
if len(arguments) > 1:
    main(arguments[1])
else:
    while True:
        code=input("AetherScript> ")
        main(code)