import os
import sys

class AetherError(Exception):
    def __init__(self, message, type_):
        self.message = message
        self.type = type_

    def __str__(self):
        return f"{self.type}: {self.message}"
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
    is_comment_open = False
    for char in chars:
        statematent += char
        match char:
            case " ":
                continue
            case "\n":
                tokens.append({ "type": "NEWLINE", "value": "\n" })
                if is_comment_open == True:
                    is_comment_open = False
                statematent = ""
            case '"' | "'" if not is_comment_open:
                if is_string_open == False:
                    statematent = ""
                    is_string_open = True
                else:
                    statematent = statematent[:-1]
                    tokens.append({ "type": "STRING", "value": statematent })
                    statematent = ""
                    is_string_open = False
            case "/" if not is_comment_open:
                if statematent[-1] == "/":
                    is_comment_open = True
                    statematent = ""
            case "(" if not is_comment_open:
                open_parenthesis += 1
                tokens.append({ "type": "LPAREN", "value": "(" })
                statematent = ""
            case ")" if not is_comment_open:
                open_parenthesis -= 1
                tokens.append({ "type": "RPAREN", "value": ")" })
                statematent = ""
            case ";" if not is_comment_open:
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
                raise AetherSyntaxError("Expected '(' after 'print'")
        elif token.get("type") == "NEWLINE":
            line+=1  
        elif token.get("type") == "SEMICOLON":
            pass
        i+=1
    return Ast
class CodeGenerator:
    def generate(self, ast):
        lines = []
        for node in ast:
            if isinstance(node, PrintNode):
                lines.append(f'print("{node.value.value}")')
        return "\n".join(lines)
def run_code(source_code):
    tokens=Lexer(source_code)
    ast= Parser(tokens)
    code = CodeGenerator().generate(ast)
    exec(code)
def main(file_path):
    source_code = read_file(file_path)
    run_code(source_code)
arguments = sys.argv
if len(arguments) > 1:
    try:
        main(arguments[1])
    except AetherError as e:
        print(e)
        sys.exit(1)
else:
    while True:
        try:
            code=input("AetherScript> ")
            run_code(code)
        except AetherError as e:
            print(e)