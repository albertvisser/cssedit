#! /usr/bin/env python3
"""CSSEditor - Start GUI
"""
import sys
from editor.main import Editor
ed = Editor()
if len(sys.argv) == 2:
    ed.open(filename=sys.argv[1])
elif len(sys.argv) == 3:
    if sys.argv[1] == "":
        ed.open(text=sys.argv[2])
    else:
        ed.open(tag=sys.argv[1], text=sys.argv[2])
# else:
#     ed.openfile()  # open()
ed.show_gui()
