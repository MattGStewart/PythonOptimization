Code Condenser
Code Condenser is a Python script that condenses and optimizes Python code to make it more concise and efficient. It does this by using abstract syntax trees (ASTs) to analyze and transform the code.

Usage
The script can be used in two ways: with a string of code or with a file containing code.

To condense a string of code, call the condense_script function and pass the code as a string argument:

python
Copy code
from code_condenser import condense_script

code = "x = 5\ny = 10\nz = x + y\nprint(z)"
condense_script(code)
This will condense the code and write it to a new file called condensed_code.py in the current directory.

To condense a file containing code, call the condense_file function and pass the file path as an argument:

python
Copy code
from code_condenser import condense_file

file_path = "/path/to/my/code.py"
condense_file(file_path)
This will condense the code in the file and write it to a new file with the same name and a .condensed extension in the same directory as the original file.

You can also specify the name of the file to write to by passing a write_to_file argument:

python
Copy code
from code_condenser import condense_script, condense_file

# condense a string of code and write it to a new file called "my_condensed_code.py"
code = "x = 5\ny = 10\nz = x + y\nprint(z)"
condense_script(code, write_to_file="my_condensed_code.py")

# condense a file and write it to a new file with a custom name
file_path = "/path/to/my/code.py"
condense_file(file_path, write_to_file="/path/to/my/condensed_code.py")
Optimization Transformations
Code Condenser applies several transformations to the code to make it more concise and efficient. These transformations include:

Replacing list comprehensions with generator expressions
Replacing range with xrange
Converting lists and tuples in membership tests to sets
Simplifying for loops with simple assignments and additions
Optimizing variable names by adding a prefix and suffix
Rounding floating point numbers to two decimal places
Optimizing binary operations by rounding floating point numbers
Optimizing string literals by removing newlines and compressing whitespace
Optimizing comments by wrapping long comments to multiple lines and removing trailing whitespace
Removing duplicate imports
Requirements
Code Condenser requires Python 3.6 or later and the ast, re, os, and decimal modules.

License
Code Condenser is released under the MIT License.
