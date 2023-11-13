class SymbolTable:
    def __init(self):
        self.symbols = {}

    def add_symbol(self, name, data_type, scope, defined):
        if name in self.symbols:
            print(f"Error: Symbol '{name}' already declared.")
        else:
            self.symbols[name] = {
                'data_type': data_type,
                'scope': scope,
                'defined': defined,
            }

    def lookup_symbol(self, name):
        return self.symbols.get(name, None)

def create_symbol_table(filename):
    sym_table = SymbolTable()
    current_scope = "Global"

    with open(filename, 'r',encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("int") or line.startswith("float") or line.startswith("string"):
                parts = line.split()
                data_type = parts[0]
                name = parts[1].strip(";")
                sym_table.add_symbol(name, data_type, current_scope, "Yes")
            elif line.startswith("void"):
                current_scope = line.split()[1].strip("(")
            elif line.startswith("}"):
                current_scope = "Global"

    return sym_table

# Read code from file and create a symbol table
file_name = "codigoBueno.txt"
symbol_table = create_symbol_table(file_name)

# Lookup symbols
print(symbol_table.lookup_symbol("x"))
print(symbol_table.lookup_symbol("v"))
print(symbol_table.lookup_symbol("n"))
print(symbol_table.lookup_symbol("y"))