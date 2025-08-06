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
    tokens = []
    statematent = ""
    open_parenthesis = 0
    count = 1
    is_string_open=False
    for char in chars:
        statematent += char
        if char == "\n":
            tokens.append({ "type": "NEWLINE", "value": "\n" })
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
class StringNode():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"StringNode: {self.value}"
class PrintNode():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"PrintNode: {self.value.__str__()}"
def Parser(tokens):
    Ast=[]
    i = 0
    line=1
    while i < len(tokens):
        token = tokens[i]
        if token.get("type") == "KEYWORD" and token.get("value") == "print":
            if tokens[i+1].get("type") == "LPAREN":
                if tokens[i+2].get("type") == "STRING":
                    Ast.append(PrintNode(StringNode(tokens[i+2].get("value"))))
                    i+=2
            else:
                AetherSyntaxError("Expected '(' after 'print'").raised(line)
        elif token.get("type") == "NEWLINE":
            line+=1  
        elif token.get("type") == "SEMICOLON":
            pass
        i+=1
    return Ast

def main(file_path):
    source_code = read_file(file_path)
    tokens=Lexer(source_code)
    Ast= Parser(tokens)
    for node in Ast:
        print(node.__str__())
arguments = sys.argv
if len(arguments) > 1:
    main(arguments[1])
else:
    while True:
        code=input("AetherScript> ")
        main(code)