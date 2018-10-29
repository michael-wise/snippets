#§
print("This is just a little proof of concept. I like the idea of parsing scripts/programs into segments.")
print("There are some things I'd like to try with it later.")
print("In this project, some_python_code.py is split into cells within a jupyter notebook.")
#§
print("The § symbols are part of utf-8 encoding (represented by '\\u00a7' in python)")
print("Unfortunately Windows Jupyter (or others?) doesn't seem to display utf-8 encode text")
print("Which is unfortunate, since python is capable of utf-8.")
print("Anyways, I used them because I think it's strange we don't use more symbols in code.")
print("It can be a dangerous road to go down, but there are probably big benefits to it if done appropriately.")
#§
print("transpile_to_jupyter.py is what does the parsing. It uses machienry in the jupyter nb lib to create this notebook.")
print("transpile_to_jupyter just looks for the commented section symbols and generates a python"
      "notebook with cells")
#§
print("It is not outfitted with much anything. Notice it even picks up empty lines at the end of the source file")



