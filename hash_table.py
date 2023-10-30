class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value

    def search(self, key):
        if key in self.table:
            return self.table[key]
        return -1

    def update(self, key, value):
        if key in self.table:
         self.table.update({key:value})
    def __str__(self):
        return str(self.table)