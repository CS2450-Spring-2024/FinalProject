import os
from pathlib import Path


MEM_SIZE = 100
TERMINAL_WORD = -99999
WORKING_DIR = Path(os.path.realpath(__file__)).parent.parent
FILETYPES = [("Text files", "*.txt"), ("All files", "*.*")]
FONT = None
# FONT = ("Arial", 12)
UVU_GREEN = "#275D38"
SECONDARY = "#B2BAB2"