import os
from pathlib import Path


WORD_SIZE = 1000
MEM_SIZE = 250
FOURDP_WORD_SIZE = 100
TERMINAL_WORD = -99999
WORKING_DIR = Path(os.path.realpath(__file__)).parent.parent
FILETYPES = [("6 Digit Programs", "*.6dp"), ("4 Digit Programs", "*.4dp"), ("Text files", "*.txt"), ("All files", "*.*")]
FONT = None
# FONT = ("Arial", 12)
UVU_GREEN = "#4C721D"
SECONDARY = "#FFFFFF"
