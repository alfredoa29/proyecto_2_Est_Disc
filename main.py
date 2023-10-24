import re

import hash_table


class Symbol:
    def __init__(self, name, type=None, line=None):
        self.name = name
        self.type = type
        self.line = line


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class VarSymbol(Symbol):
    def __init__(self, name, type, line=None):
        super().__init__(name, type, line)

    def __str__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', type='{self.type}', line='{self.line}')>"

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self):
        self._symbols = hash_table.HashTable(10)

    def store(self, symbol):
        print('Define: %s' % symbol)
        self._symbols.insert(symbol.name, symbol)

    def search(self, key):
        print('Lookup: %s' % key)
        symbol = self._symbols.search(key)
        return symbol

    def __str__(self):

        return str(self._symbols.__str__())

    def openFile(self):
        return self._openFile("codigoBueno.txt")


    ''' this method reads a file from a txt and those lines are added to a list to be processed later by other methods.'''


    def _openFile(self, fileName):
        line_number = 0
        scope = "global"
        lines = []
        try:
            with open(fileName, "r", encoding="utf-8") as file:

                for line in file:
                    lines.append(line.strip())

        #exceptions to handle exceptions and they are easier to fix problems

        except FileNotFoundError:
            print(f"File '{fileName}' not found.")
        except Exception as e:
            print(f"An error occurred in method openfile: {e}")
        return lines

    def createSymbolTable(self):
        self._createSymbolTable(self.openFile())

    def _createSymbolTable(self, list_of_lines):

        line_number = 0
        scope = "global"
        try:
            for line in list_of_lines:
                line_number += 1
                if line.startswith("int") or line.startswith("float") or line.startswith("string"):
                    line = re.split(r"[(\,\=\)\' ']", line)
                    data_type = BuiltinTypeSymbol(line[0])
                    name = line[1].strip(";")

                    if self._cheIfNameAlreadyExists(name):
                        self._symbols.insert(name, VarSymbol(name, data_type, line_number))
                    else:
                        print(f"ERROR-in line {line_number}: the name '{name}' already exists.")

                elif line.startswith("void"):
                    fullLine = line;
                    line = re.split(r"[(\,\)\' ']", line)
                    data_type = BuiltinTypeSymbol(line[0])
                    name = line[1].strip(";")
                    if self._cheIfNameAlreadyExists(name):
                       self._symbols.insert(name, VarSymbol(name, data_type, line_number))
                    else:
                         print(f"ERROR- in line {line_number}: the name '{name}' already exists.")

                    self._checkVarsInsideFunction(fullLine,line_number)


        except Exception as e:
            print(f"An error occurred in method _createSymbolTable: {e}")

    '''This method cheks if the variables exist in the symbol table and if it does not exist in the symbol table it returns -1
    and returns false'''
    def _cheIfNameAlreadyExists(self, name):
        return self.search(name) == -1

    def _checkVarsInsideFunction(self, line, line_number):

        try:
            #tries to find the vars inside the parerhesis of the method like '(float v, string n)'
             findParenthesis = re.findall(r'\(.*?\)', line)
            #it goes 	through the findParenthesis list and split the variables with the pattern ','
             for word in findParenthesis:
               vari = re.split(r"[,]", word)

               for words in vari:
                    # it goes through words and get the var name and var type
                     if words.find("float") or words.find("int") or words.find("string"):
                         splitVar = words.split()
                         #with .strip remove the parenthesis of the name or type
                         data_type = BuiltinTypeSymbol(splitVar[0].strip('('))
                         name = splitVar[1].strip(')')


                         if self._cheIfNameAlreadyExists(name):
                            self._symbols.insert(name, VarSymbol(name, data_type, line_number))
                         else:
                            print(f"ERROR- in line {line_number}: the name '{name}' already exists.")









        except Exception as e:
            print(f"An error occurred in method _checkVarsInsideFunction: {e}")
        return

symbol_table = SymbolTable()
symbol_table.createSymbolTable()
print(symbol_table)
