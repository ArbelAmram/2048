# This file is referring 'assets' folder as a python package
# When a file from 'assets' is imported __init__.py file will run first

from .design import *

print("__init__.py ran from assets")