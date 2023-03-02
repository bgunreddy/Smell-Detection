import os
import ast
import sys
import rope.base.project
import rope.base.libutils
import rope.base.codeanalyze
from pylint.lint import Run
from collections import defaultdict


def detect_long_methods(file_path, max_lines=20):
    """
    Detects long method smell in a given code file by checking if any of its functions
    have more than max_lines lines of code.
    
    :param file_path: the path to the code file
    :param max_lines: the maximum number of lines a function can have before it is considered
                      to have long method smell (default is 20)
    :return: a list of tuples, where each tuple contains the name of a function and the
             number of lines of code it has


    Explination :
    This function uses the ast module to parse the code file into an abstract syntax tree (AST), 
    and then walks the tree to find all the FunctionDef nodes (which represent functions). 
    For each function, it calculates the number of lines of code it has by subtracting 
    the starting line number of its body from the ending line number of its body, and adding 1 
    (to account for the final newline). If the number of lines is greater than max_lines, it adds 
    the function's name and number of lines to a list of long methods.
    """
    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)
    
    long_methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            num_lines = node.body[-1].lineno - node.body[0].lineno + 1
            if num_lines > max_lines:
                long_methods.append((node.name, num_lines))
    
    return long_methods


def detect_large_classes(file_path, max_methods=10, max_attributes=10):
    """
    Detects large class smell in a given code file by checking if any of its classes
    have more than max_methods methods or more than max_attributes attributes.
    
    :param file_path: the path to the code file
    :param max_methods: the maximum number of methods a class can have before it is considered
                        to have large class smell (default is 10)
    :param max_attributes: the maximum number of attributes a class can have before it is considered
                           to have large class smell (default is 10)
    :return: a list of tuples, where each tuple contains the name of a class, the number of methods
             it has, and the number of attributes it has

    Explination :
    This function uses the ast module to parse the code file into an abstract syntax tree (AST), 
    and then walks the tree to find all the ClassDef nodes (which represent classes). For each class, 
    it calculates the number of methods it has by subtracting the number of FunctionDef nodes from the 
    total number of nodes in its body, and the number of attributes it has by subtracting the number of 
    methods from the total number of nodes. If either of these numbers is greater than the respective maximum 
    threshold, it adds the class's name, number of methods, and number of attributes to a list of large classes.
    """
    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)
    
    large_classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            num_methods = len(node.body) - sum(isinstance(x, ast.FunctionDef) for x in node.body)
            num_attributes = len(node.body) - num_methods
            if num_methods > max_methods or num_attributes > max_attributes:
                large_classes.append((node.name, num_methods, num_attributes))
    
    return large_classes

def detect_duplicate_code(filename):
    # Read the contents of the specified file
    with open(filename, 'r') as file:
        code = file.read()

    # Convert the code into an abstract syntax tree (AST)
    tree = ast.parse(code)

    # Define a visitor class to visit all FunctionDef nodes in the AST
    class CodeVisitor(ast.NodeVisitor):
        def __init__(self):
            # Initialize empty lists to store extracted code and line numbers
            self.codes = []
            self.lines = []

        def visit_FunctionDef(self, node):
            # Extract the body of the function and split it into a list of lines
            code = ast.unparse(node.body)
            code = [line.strip() for line in code.split('\n') if line.strip()]
            # Append the code and starting line number to the corresponding lists
            self.codes.append(code)
            self.lines.append(node.lineno)

        def get_duplicates(self):
            # Initialize an empty list to store any duplicate code smells
            duplicates = []
            # Check each pair of code lists for duplicates
            for i, code1 in enumerate(self.codes):
                for j, code2 in enumerate(self.codes[i+1:]):
                    if code1 == code2:
                        # If a duplicate is found, append the starting line numbers of both functions
                        duplicates.append((self.lines[i], self.lines[i+j+1]))
            # Return the list of duplicate code smells
            return duplicates

    # Create an instance of the CodeVisitor class and visit the AST
    visitor = CodeVisitor()
    visitor.visit(tree)
    # Get the list of duplicate code smells
    duplicates = visitor.get_duplicates()

    return duplicates



# Function to recursively search a directory for Python files and detect code smells
def detect_smells_in_directory(directory):
    smells = defaultdict(list)
    project = rope.base.project.Project(directory)
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                with open(filepath) as f:
                    code = f.read()

                long_methods = detect_long_methods(filepath)

                if long_methods:
                    smells['Long Method'].append((filepath, long_methods))
                    print(f'Long Method detected in file {filepath} on line(s) {[smell for smell in long_methods]}\n\n')
                else:
                    print(f"Long Method smell does not exits in file {filepath} on line(s)\n\n")

                large_classes = detect_large_classes(filepath)
                if large_classes:
                    smells['Large Class'].append((filepath, large_classes))
                    print(f'Large Class detected in file {filepath} on line(s) {[smell for smell in large_classes]}\n\n')
                else:
                    print(f"Large Class smell does not exits in file {filepath} on line(s)\n\n")

                duplicate_lines = detect_duplicate_code(filepath)
                if duplicate_lines:
                    smells['Duplicate Code'].append((filepath, duplicate_lines))
                    print(f'Duplicate Code detected in file {filepath} on line(s) {duplicate_lines}\n\n')
                else:
                    print(f"Duplicate Code smell does not exits in file {filepath} on line(s)\n\n")

                print(".........................||.........................\n\n\n")


    return smells

def main():
    # Get the directory path from the command line arguments
    if len(sys.argv) < 2:
        print("Usage: detect_smells.py <directory>")
        return

    directory = sys.argv[1]

    # Analyze the directory for code smells
    smells = detect_smells_in_directory(directory)


if __name__ == '__main__':
    main()

