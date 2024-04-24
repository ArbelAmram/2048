# This file is referring 'entities' folder as a python package
# When any file from 'entities' is imported __init__.py file will run first

from .tile import Tile

print("__init__.py ran from entities")