#! /usr/bin/env python3
import sys
## from editor.csseditor_qt4 import main
from editor.csseditor_qt import main
if len(sys.argv) == 2:
    main(filename=sys.argv[1])
elif len(sys.argv) == 3:
    if sys.argv[1] == "":
        main(text=sys.argv[2])
    else:
        main(tag=sys.argv[1], text=sys.argv[2])
else:
    main()

