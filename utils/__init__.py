# This file is referring 'utils' folder as a python package
# When a file from 'utils' is imported __init__.py file will run first 

from .helpers import draw, generate_tiles, move_tiles

print("__init__.py ran from utils")