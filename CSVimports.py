import csv
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from datetime import datetime as dt
import datetime

class RowHandler:
    def __init__(self) -> None:
        self.importCols = []
        self.colTypes = {}
        self._currentRow = {}
        self._data = []
        self.defineFields = {}
        self._index = 0

    def Index(self):
        return self._index

    def ColsFromString(self, st):
        self.importCols = [a.strip() for a in st.split(',')]

    def Value(self, tag: str):
        if tag not in self._currentRow.keys(): 
            raise Exception(f'Tag "{tag}" not found.')

        if tag in self.colTypes.keys():
            return  self.colTypes[tag](self._currentRow[tag])

        return self._currentRow[tag]

    def ValueOut(self, tag):
        def Escape(s):
            return "N'" + s.replace("'", "''") + "'"
        if tag in self.defineFields.keys(): 
            val = self.defineFields[tag]()
        else: val = self.Value(tag)
        if isinstance(val, str): return Escape(val)
        return str(val)

    def Ref(self, tag):
        return lambda: self.Value(tag)

    def Load(self):
        def DataTypes(header, data):
            def ArrayType(array):
                def IsInt(a):
                    try: 
                        if a == 'NULL' or (int(a) == 0 or a[0] != '0'): return True
                    except: pass
                    return False
                def IsFloat(a):
                    try: 
                        if a == 'NULL': return True
                        float(a)
                        return True
                    except: pass
                    return False

                if all(map(IsInt, array)): return int
                if all(map(IsFloat, array)): return float
                return str

            return {tag: ArrayType([row[tag] for row in data]) for tag in header} 
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV Documents","*.csv"), ("All Files","*.*")])

        with open(file_path, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f, delimiter=',')
            data = list(reader)

        self._data = data
        header= data[0].keys()
        self.colTypes = DataTypes(header, data) | self.colTypes

    def DefineCols(self, di):
        self.defineFields = {
            key: (lambda: (di[key])) for key in di.keys()
        }

    def Output(self) -> str:
        out = ''
        for i, row in enumerate(self._data):
            self._currentRow = row
            self._index = i
            out += '(' + ', '.join([self.ValueOut(tag) for tag in self.importCols]) + '), \n'

             # f.write('(' + ', '.join([Pad(a) for a in row]) + '), \n')
        # f.write('(' + ', '.join(["01" + f'{i:0>18}'] + [Pad(a) for a in row[:2] + row[5:6] ]) + '), \n')
        
        save = asksaveasfile(initialfile = 'Values list.txt',
            defaultextension=".txt",filetypes=[("Text Documents","*.txt"), ("All Files","*.*")])

        with open(save.name, 'w', encoding='utf8', newline='') as f:
            f.write(', '.join(self.importCols) + '\n')
            f.write(out)
        
class Format:
    def LoadId(number: int, length = 18, prefix = '01' ) -> str:
        return prefix + f'{str(number).zfill(length)}'
    def Now():
        return str(dt.now())[:23]

    def Date(date_str, format_str = r'%d/%m/%Y'):
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        return str(datetime_obj.date())

