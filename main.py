from CSVimports import RowHandler, Format
rh = RowHandler(); v = rh.Value

# There's an internal logic for deciding the types
# but you can force each column to load into a selected type.
rh.colTypes = {
# Example: 'SKU': str,
}
rh.Load()

# Define a function to process data, either before define a function this command or use lambda.
# Lambda is a function with no name, eg. "lambda x, y: x+y" for summing two numbers.
# v(<tag>) returns the row's value, eg. v('QTY'); the Format class consists of formatting functions for convenience.

rh.defineFields = {
# Example: 'employee_id':lambda:  rh.Index()
# Example: 'employee_id':lambda:  Format.LoadId(rh.Index() + 300),
# Example: 'full_name': lambda: v('firstname') + ' ' + v('lastname')
# Example: 'add_date': lambda: Format.Now(),
}

# Example: employee_id, full_name, add_date
rh.ColsFromString('''

''')

rh.Output()