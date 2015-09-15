import sys
from editor.cssedit_qt import main
if len(sys.argv) == 2:
    main(filename=sys.argv[1])
elif len(sys.argv) == 3:
    if sys.argv[1] == "":
        main(text=sys.argv[2])
    else:
        main(tag=sys.argv[1], text=sys.argv[2])
else:
    main(sys.argv)

