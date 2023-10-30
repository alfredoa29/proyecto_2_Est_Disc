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

    def __init__(self, name, type, line=None, is_func = False): #if it is a function like int foo() it is_fun is true
        super().__init__(name, type, line)
        self.var_func = is_func
    def __str__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', type='{self.type}', line='{self.line}')>"

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self):
        self._symbols = hash_table.HashTable()
        self.mathSymbols = {'=': '=', '+':'+', '-':'-'}
        self.scopeStack = ScopeSymbolStack()
        self.function_name = "" #name of the current funcion exampple: int foo()
    def store(self, symbol):
        #print('Define: %s' % symbol)
        self._symbols.insert(symbol.name, symbol)

    def search(self, key):
        #print('Lookup: %s' % key)
        symbol = self._symbols.search(key)
        return symbol

    def lookup(self, key):
        if key in self.mathSymbols:
            return  True
        return False
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
        #scopeStack = ScopeSymbolStack()
        try:
            joing_lines = ''.join(list_of_lines)
            for index, line in enumerate(list_of_lines):

                line_number = index #it counts the different lines and is added to the object inside the stack
                fullLine = line

                #pattern to match correct line code (int x = 10)
                pattern = r'(int|float|string|void)\s+(\w+)\s*([=(])'
                # pattern to match incorrect line code without var ( x = 10)
                pattern3 = r'(\w+)\s*=\s*(\d+)'
                matches_correct_code = re.findall(pattern, line)
                matches_no_var = re.findall(pattern3, line)

                data_type = None
                variable_name = None
                delimiter = None

                no_var_name = None
                no_delimiter = None

                    #matches the code with vars and = ( var = 10
                for match in matches_correct_code:
                    data_type , variable_name, delimiter = match
                # matches the code without vars x = 10
                for match in matches_no_var:
                      no_var_name, no_delimiter = match


                if  self._cheIfNameAlreadyExists(no_var_name) and no_delimiter != None:
                        print(f"ERROR-in line {line_number}: the name '{no_var_name}' has not been declared.")

                if data_type == "int" or data_type == "float" or data_type == "string" or data_type == "void":



                    if delimiter == '=':
                        var_type= BuiltinTypeSymbol(data_type)
                        name = variable_name
                        if self._cheIfNameAlreadyExists(name):
                            self._symbols.insert(name, VarSymbol(name, var_type, line_number)) #_symbols has global hashtable
                            scope = ScopeSymbol(1, "global", self._symbols)

                            self.scopeStack.push(scope)
                            print( self.scopeStack)

                        else:
                            print(f"ERROR-in line {line_number}: the name '{name}' already exists.")

                    if delimiter == '('  :
                                line = re.split(r"[(\,\)\' ']", fullLine)
                                var_type = BuiltinTypeSymbol(data_type)
                                name = variable_name
                                line_number =+ 1
                                if self._cheIfNameAlreadyExists(name):
                                    methodHashTable = hash_table.HashTable()
                                    self._symbols.insert(name, VarSymbol(name, var_type, line_number,True ))
                                    scope = ScopeSymbol(1, "global", self._symbols)
                                    self.function_name = name

                                    self.scopeStack.push(scope) #it adds int foo
                                    print(self.scopeStack)

                                else:
                                    print(f"ERROR-in line {self.check_var_exists_inside_table(list_of_lines, name)}: the name '{name}' already exists.")
                                methodHashTable = hash_table.HashTable()

                                #it checks if there are vars inside the mthodscope  int funcion(float v, string n)
                                self._checkVarsInsideFunction(fullLine, line_number, methodHashTable)
                                scope = ScopeSymbol(2, name, methodHashTable)
                                self.scopeStack.push(scope)

                                join_line = fullLine.join(fullLine)
                                pattern = r'(\s*if\s*\([^{}]*\)|{[^{]*})'
                                matches_correct_code = re.findall(pattern, joing_lines, re.DOTALL)
                                for match in matches_correct_code:
                                    cont_inside_brces = match
                                    line_number_inside_brces = line_number+1

                                    pattern = r'(int|float|string|return)\s+(\w+)\s*='


                                    # Find all matches for variable declarations within the current scope
                                    matches2 = re.finditer(pattern, cont_inside_brces)

                                    # Initialize a list to store int variables within the current scope
                                    int_variables_in_scope = []
                                    innerHasTable = hash_table.HashTable()
                                    scope = ScopeSymbol(3, "inner", innerHasTable)
                                    for matchIn in matches2:
                                        line_number_inside_brces =+ 1
                                        data_type, variable_name = matchIn.groups()
                                        if data_type == 'int':
                                            name = variable_name.strip(";")
                                            int_variables_in_scope.append(name)
                                            innerHasTable.insert(name, VarSymbol(name, data_type, line_number))
                                            scope = ScopeSymbol(3, "inner", line_number_inside_brces+1)
                                            self.scopeStack.push(scope)
                                        if data_type == 'float':
                                            name = variable_name.strip(";")
                                            int_variables_in_scope.append(name)
                                            innerHasTable.insert(name, VarSymbol(name, data_type, line_number))
                                            scope = ScopeSymbol(3, "inner", line_number_inside_brces+1)
                                            self.scopeStack.push(scope)

                                        if data_type == 'string':
                                            name = variable_name.strip(";")
                                            int_variables_in_scope.append(name)
                                            innerHasTable.insert(name, VarSymbol(name, data_type, line_number))
                                            scope = ScopeSymbol(3, "inner", line_number_inside_brces+1)
                                            self.scopeStack.push(scope)
                                            # creo que voy a borrar esto
                                        if  data_type == 'return':
                                            print('return')

                                    self.scopeStack.push(scope)
                                #it matches the return value from the
                                pattern_return = r'(return)\s+(\w+)'
                                match_return = re.findall(pattern_return, match)
                                for match_r in match_return:

                                    return_name, return_var = match_r
                                    if not self.chek_return_var(return_var):
                                        print(f"ERROR-in line {self.find_line_of_code(list_of_lines,'return' )}: the return value '{return_var}' does not match with de declaration of {self.function_name}")



                                    # if there is a } so it pops a element from the stack
                                    for match_bra in matches_correct_code:
                                        if '}' in match_bra:
                                            self.scopeStack.pop()
                                    print("Content inside braces:")
                                    print(cont_inside_brces)
                                    print("Int Variables in this scope:")
                                    print(int_variables_in_scope)

                                    self.check_var_exists_inside_table(cont_inside_brces, line_number_inside_brces, list_of_lines)

                                # if there is a } so it pop a element from the stack
                                for match_bra in matches_correct_code:
                                    if '}' in match_bra:
                                        self.scopeStack.pop()





        except Exception as e:
            print(f"An error occurred in method _createSymbolTable: {e}")

    '''This method cheks if the variables exist in the symbol table and if it does not exist in the symbol table it returns -1
    and returns false'''
    def _cheIfNameAlreadyExists(self, name):
        return self.search(name) == -1

    def _checkVarsInsideFunction(self, line, line_number, hashtable):

        try:
            #tries to find the vars inside the parerhesis of the method like '(float v, string n)'
             find_parenthesis = re.findall(r'\(.*?\)', line)
            #it goes 	through the findParenthesis list and split the variables with the pattern ','
             for word in find_parenthesis:
               vari = re.split(r"[,]", word)

               for words in vari:
                    # it goes through words and get the var name and var type
                     if words.find("float") or words.find("int") or words.find("string"):
                         splitVar = words.split()
                         #with .strip remove the parenthesis of the name or type
                         data_type = BuiltinTypeSymbol(splitVar[0].strip('('))
                         name = splitVar[1].strip(')')



                         hashtable.insert(name, VarSymbol(name, data_type, line_number))
                         #else:
                          #  print(f"ERROR- in line {line_number}: the name '{name}' already exists.")


        except Exception as e:
            print(f"An error occurred in method _checkVarsInsideFunction: {e}")
        return hashtable


    '''
    it checks if the variables inside the function exists in the hashtable, but firts it goes to the stack and itarites it
    '''
    def check_var_exists_inside_table(self, line, line_number, list_of_lines):

        pattern = r'\b[^\d\W]\w*\b(?=\s*=\s*[^=])'
        matches = re.finditer(pattern, line)

        for match in matches:
            var_name = match.group().rstrip('=').strip()
            find =   self.scopeStack.find(var_name)
            print(var_name)
            if find ==  None:
                print(f"ERROR-in line {line_number}:  variable " + var_name + " not declared")


    def chek_return_var(self, var_name):

        return_var = self.scopeStack.find(var_name)
        method_var = self.scopeStack.find(self.function_name)
        if method_var.type == return_var.type:
         return True
    ''' the function checks the list of lines from the txt and tries to match  the var or methods and return the # of the line that it is'''
    def find_line_of_code(self, word_list, word_to_find):
        for index, word in enumerate(word_list):
            pattern = r'\b' + word_to_find + r'\b'
            find = re.search(pattern, word)
            if find:
                return index
        return -1


class ScopeSymbol(SymbolTable):

     def __init__(self, scopeLevel, scopeName, scopeTables):
         self._scopeLevel = scopeLevel
         self._scopeName = scopeName
         self._scopeTables = scopeTables

     def __str__(self):
         return f"Scope: Level {self._scopeLevel}, Name '{self._scopeName}'"

     def find_in_scope_tables(self, key):

         result = self._scopeTables.search(key)
         return result


class ScopeSymbolStack():
    def __init__(self):
        self.stackSymbolTable = []

    ''' push or updte. if it finds the same scope name in the stack, it will update the scope, so only wil be 3 scopes'''
    def push(self, scopeSymbol):

        if scopeSymbol._scopeLevel in self.stackSymbolTable:
             index = self.stackSymbolTable.index(scopeSymbol)
             old_element = self.stackSymbolTable.pop(index)
             updated_element = scopeSymbol
             self.stackSymbolTable.insert(index, updated_element)
        else:
             self.stackSymbolTable.append(scopeSymbol)



    def pop(self):
        if self.stackSymbolTable:
            return self.stackSymbolTable.pop()
        return None

    def lookup_scope(self, name):
        for scope in reversed(self.stack):
            if name in scope:
                return scope[name]
        return None

    def pop(self):
        if(self.isEmpty()):
            return "stack is empty"
        else:
            return self.stackSymbolTable.pop()

    def isEmpty(self):
        return len(self.stackSymbolTable) == 0

    def find(self, name):
        for scope in reversed(self.stackSymbolTable):
            result = scope.find_in_scope_tables(name)
            if result != -1:
                return result
        return None



    def __str__(self):

        return f""






symbol_table = SymbolTable()
symbol_table.createSymbolTable()
#print(symbol_table)
