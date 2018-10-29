import nbformat as nbf
from nbformat.v4.nbjson import JSONWriter
import re

nbcellbuffer = []
blockbuffer = []
with open("some_python_code.py", encoding='utf-8') as fp:
    for line in fp:
        print(line)
        if re.search(r'#§', line):
            nbcellbuffer.append(''.join(blockbuffer)) if blockbuffer else None
            blockbuffer = []
        else:
            blockbuffer.append(line)
    nbcellbuffer.append(''.join(blockbuffer))

cells = [nbf.v4.new_code_cell(execution_count = 0, source=ele) for ele in nbcellbuffer]
nb = nbf.v4.new_notebook(cells=cells)

with open ('output.ipynb', 'w') as f:
    writer = JSONWriter()
    writer.write(nb, f)

# '§'=='\u00a7'