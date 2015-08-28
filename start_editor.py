import sys
from editor.cssedit_qt import main
if len(sys.argv) != 1:
    main(filename=sys.argv[1])
else:
    main()

